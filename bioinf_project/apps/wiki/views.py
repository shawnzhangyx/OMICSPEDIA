import re
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from utils import diff_match_patch
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


from .forms import PageForm, PageRevisionForm, PageCommentForm
from .models import Page, PageRevision, PageComment, UserPage
import markdown
import json
# Create your views here.


class IndexView(TemplateView):
    template_name = "wiki/wiki_index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        SLICE = 5
        all = Page.objects.all()
        bookmarked = all.order_by('-bookmark_count')[:SLICE]
        viewed = all.order_by('-view_count')[:SLICE]
        commented = all.filter(comment_count__gt = 0).order_by('-comment_count')[:SLICE]
        longest = all.order_by('-current_revision__total_chars')[:SLICE]
        shortest = all.order_by('current_revision__total_chars')[:SLICE]
        update = PageRevision.objects.order_by('-modified_date')[:8]
        workflow = all.filter(wiki_tag__categories = 1)[:SLICE]
        context['bookmark'] = bookmarked
        context['view'] = viewed
        context['comment'] = commented
        context['longest'] = longest
        context['shortest'] = shortest
        context['update'] = update
        context['workflow'] = workflow
        context['page_total'] = all.count()
        return context
        
class WikiListView(ListView):
    #model = Page
    template_name = "wiki/wiki_list.html"
    context_object_name = "wiki_list"
    paginate_by = 30
    
    def get_queryset(self): 
        tab = self.request.GET.get('tab') or 'View'
        if tab == "Workflow":
            return Page.objects.all().filter(wiki_tag__categories =1).order_by('-view_count')
        dict = {'Bookmark':'-bookmark_count', 'View':'-view_count', 'Comment':'-comment_count', 'Longest':'-current_revision__total_chars', 'Shortest':'current_revision__total_chars'}
        return Page.objects.all().order_by(dict[tab])
    
    def get_context_data(self, **kwargs):
        context = super(WikiListView, self).get_context_data(**kwargs)
        context['tab'] = self.request.GET.get('tab') or 'Bookmark'
        return context
    
class PageRevisionListView(ListView):
    template_name = "wiki/wiki_revision_list.html"
    context_object_name = "revision_list"
    paginate_by = 50
    
    def get_queryset(self):
        return PageRevision.objects.order_by('-modified_date')
    
class WikiNew(CreateView):
    template_name = "wiki/wiki_new.html"
    form_class = PageForm
    
    @method_decorator(permission_required("wiki.add_page", login_url="/accounts/email-verification/"))
    def dispatch(self, *args, **kwargs):
        return super(WikiNew, self).dispatch(*args, **kwargs)
        
    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        if 'title' in self.request.GET:
            kwargs['initial'].update({'title':self.request.GET['title']})
        return form_class(**kwargs)
    
    def form_valid(self, form):
        form.save()
        new_revision = PageRevision(content=form.cleaned_data['content'],
                       revision_summary='',
                       page=form.instance, author=self.request.user)
        new_revision.save()
        form.instance.current_revision=new_revision
        return super(WikiNew, self).form_valid(form)
    
    def get_success_url(self):
        if self.request.GET.get('next'):
            return redirect(self.request.GET['next'])
        return super(WikiNew,self).get_success_url()
    

class WikiEdit(UpdateView):
    form_class = PageRevisionForm
    template_name = 'wiki/wiki_edit.html'

    @method_decorator(permission_required("wiki.change_page", login_url="/accounts/email-verification/"))
    def dispatch(self, *args, **kwargs):
        return super(WikiEdit, self).dispatch(*args, **kwargs)
        
    def get_object(self):
        return Page.objects.get(title=self.kwargs['title'].replace('_', ' '))

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'content':self.object.current_revision.content})
        return form_class(**kwargs)

    def form_valid(self, form):
        if form.cleaned_data['content'] != self.object.current_revision.content:
            new_revision = PageRevision(content=form.cleaned_data['content'],
                       revision_summary=form.cleaned_data['summary'],
                       page=self.object, author = self.request.user)
            new_revision.save()
            self.object.current_revision=new_revision
            self.object.save()
        return super(WikiEdit, self).form_valid(form)

    def get_context_data(self, **kwargs):
       context = super(WikiEdit, self).get_context_data(**kwargs)
       if 'preview' in self.request.session:
           context['preview'] = markdown.markdown(self.request.session['preview'],
                   extensions=['extra','wikilinks(base_url=/wiki/, end_url=/)','toc'])
           #context['form'].initial['content'] = self.request.session['preview']
           context['content'] = self.request.session['preview']
           del self.request.session['preview']
       return context

@permission_required("wiki.change_page", login_url="/accounts/email-verification/")
def wiki_section_edit(request, **kwargs):
    header = request.GET.get('header')
    section = request.GET['name']
    section = re.escape(section)
    # Find the associate wiki and its most current content. 
    page = Page.objects.get(title=kwargs['title'].replace('_', ' '))

    if request.method == "GET":
        page_content = page.current_revision.content
        # find the header level
        header_level = header[1]
        # compile the re pattern
        pattern = re.compile(u'(^|\r\n)(#{'+header_level+u'}\s*'+section+ '(.|\n)*?)(\r\n#{'+header_level+u'}[^#]|$)')
        match = re.search(pattern, page_content)
        section_content = match.group(2)
        return render(request, 'wiki/wiki_edit_section.html',{'page':page,'header':header,'section':section, 'content':section_content})
    elif request.method=="POST":
        page_content = page.current_revision.content
        section_content = request.POST.get('content')
        header_level = header[1]
        pattern = re.compile(u'(^|\r\n)(#{'+header_level+u'}\s*'+section+ '(.|\n)*?)(\r\n#{'+header_level+u'}[^#]|$)')
        match = re.search(pattern, page_content)
        revised_page_content = re.sub(pattern, match.group(1) +section_content + match.group(4), page_content)
        # if there is no summary
        if not request.POST.get('summary'):
           summary_errors = 'This field is required' 
           return render(request, 'wiki/wiki_edit_section.html',{'page':page,'header':header,'section':section, 'content':section_content, 'summary_errors':summary_errors})
           
        if revised_page_content != page_content:
            new_revision = PageRevision(content=revised_page_content,
                       revision_summary=request.POST.get('summary'), 
                       page=page, author = request.user)
            new_revision.save()
            page.current_revision=new_revision
            page.save()
        #return render(request, 'wiki/wiki_edit_section.html',{'page':page,'header':header,'section':section, 'content':revised_page_content})
        return HttpResponseRedirect(reverse("wiki:wiki-detail", kwargs={'title':kwargs['title']}))
    #pat = re.compile(u'(^|\r\n)(#\s+section 2(.|\n)*?)(\r\n#[^#]|$)') # stop when reach next section, the end of file,or higher level of section. 


class WikiDetails(DetailView):
    template_name = "wiki/wiki_detail.html"
    model = Page

    def dispatch(self, *args, **kwargs):
        try: Page.objects.get(title=self.kwargs['title'].replace('_', ' '))
        except Page.DoesNotExist:
            #return HttpResponseRedirect(reverse("wiki:wiki-new"))
            return render(self.request, 'wiki/wiki_not_found.html',{'title':self.kwargs['title'].replace('_',' ')})
        else: page = Page.objects.get(title=self.kwargs['title'].replace('_', ' '))
        # if this page has a redirect_to, then redirect to the duplicated page. 
        if page.redirect_to: 
            return HttpResponseRedirect(reverse('wiki:wiki-detail', kwargs={'title':page.redirect_to.get_title()}))
        else:
            return super(WikiDetails, self).dispatch(*args, **kwargs)

    def get_object(self):
        obj = Page.objects.get(title=self.kwargs['title'].replace('_', ' '))
        Page.update_wiki_views(obj, request=self.request)
        return obj

    def get_context_data(self, **kwargs):
        context = super(WikiDetails, self).get_context_data(**kwargs)
        context['comment_list'] = self.object.comments.order_by('-last_modified')
        return context
    #need to display everything in the same subject.

class WikiHistory(ListView):
    model = PageRevision
    template_name = "wiki/wiki_revision_history.html"
    context_object_name = "revision_list"
    paginate_by = 25
    
    def get_queryset(self):
        return PageRevision.objects.filter(page__title = self.kwargs['title'].replace('_', ' ')).order_by('-modified_date')

    def get_context_data(self, **kwargs):
        context = super(WikiHistory, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(title = self.kwargs['title'].replace('_', ' '))
        return context 


class WikiDiff(DetailView):
    model = PageRevision
    template_name = "wiki/wiki_diff.html"

    def get_diff(self):
        text2 = self.object.content
        if self.object.get_pre_revision():
            text1 = self.object.get_pre_revision().content
        else:
            text1 = ""
        func = diff_match_patch.diff_match_patch()
        diff = func.diff_main(text1, text2)
        func.diff_cleanupSemantic(diff)
        htmldiff = func.diff_prettyHtml(diff)
        return htmldiff
    def get_context_data(self, **kwargs):
        context = super(WikiDiff, self).get_context_data(**kwargs)
        context['diff'] = self.get_diff()
        context['page'] = self.object.page
        return context
    

class WikiCommentView(DetailView):
    model = Page
    template_name = "wiki/wiki_comment.html"
    
    def get_object(self):
        return Page.objects.get(title=self.kwargs['title'].replace('_', ' '))
        
    def get_context_data(self, **kwargs):
        context = super(WikiCommentView, self).get_context_data(**kwargs)
        comment_list = self.object.comments.order_by('-modified')
        context['open_comment_list'] = comment_list.filter(status = 0)
        context['pending_comment_list'] = comment_list.filter(status = 1)
        context['closed_comment_list'] = comment_list.filter(status = 2)
        return context
        
class WikiCommentAdd(CreateView):
    model = PageComment
    template_name = "wiki/wiki_comment_edit.html"
    
    @method_decorator(permission_required("wiki.add_pagecomment", login_url="/accounts/email-verification/"))
    def dispatch(self, *args, **kwargs):
        return super(WikiCommentAdd, self).dispatch(*args, **kwargs)
        
    def get_form_kwargs(self):
        kwargs = super(WikiCommentAdd, self).get_form_kwargs()
        page = Page.objects.get(title=self.kwargs['title'].replace("_", " " ))
        post_data = kwargs['data'].copy()
        post_data.update({'status':0,
                          'comment_type':0,
                          'author':self.request.user.id,
                          'created':timezone.now(),
                          'init_revision': page.current_revision.id,
                          'page': page.id})
        kwargs['data'] = post_data
        #form.instance.comment_type = 0
        #form.instance.page = self.kwargs['page']
        #form.instance.author = self.user
        #form.instance.created = timezone.now()
        return kwargs

class WikiCommentEdit(UpdateView):

    #model = PageComment
    form_class = PageCommentForm
    template_name = "wiki/wiki_comment_edit.html"
    #fields = ['status','issue','detail']
    
    @method_decorator(permission_required("wiki.change_pagecomment", login_url="/accounts/email-verification/"))
    def dispatch(self, *args, **kwargs):
        return super(WikiCommentEdit, self).dispatch(*args, **kwargs)

    def get_object(self):
        return PageComment.objects.get(pk= self.kwargs['pk'])

    #def get_form(self):
        
    
class UserPageView(ListView):
    template_name = "wiki/wiki_userpage.html"
    context_object_name = "userpage_list"
    
    def get_queryset(self):
        return UserPage.objects.filter(page__title=self.kwargs['title'].replace('_', ' ')).order_by('-added')
        
    def get_context_data(self, **kwargs):
        context = super(UserPageView, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(title=self.kwargs['title'].replace('_',' '))
        return context
    
        
def wikilinks(request):
    context = RequestContext(request)
    if request.method=="GET":
        titles = request.GET.getlist('titles[]')
        response = []
        #return HttpResponse(json.dumps({'number':titles}))
        for title in titles:
            try: obj = Page.objects.get(title=title.replace('_', ' '))
            except Page.DoesNotExist:
                response.append('0')
            #return 0 # if the wikilinks does not exist.
            else:
                response.append('1')
        return HttpResponse(json.dumps({'response':response}))
            #return 1 # if the wikilinks existself.
