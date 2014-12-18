import re
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from utils import diff_match_patch
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .forms import PageForm, PageRevisionForm
from .models import Page, PageRevision, PageComment, UserPage
import markdown
import json
# Create your views here.


class IndexView(ListView):
    model = Page
    template_name = "wiki/index.html"
    context_object_name = "wiki_list"

class WikiNew(CreateView):
    template_name = "wiki/wiki_new.html"
    form_class = PageForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WikiNew, self).dispatch(*args, **kwargs)
        
    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        if 'title' in self.request.GET:
            kwargs['initial'].update({'title':self.request.GET['title']})
        return form_class(**kwargs)
    
    def form_valid(self, form):
        form.save()
        new_revision = PageRevision(content=self.request.POST['content'],
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WikiEdit, self).dispatch(*args, **kwargs)
        
    def get_object(self):
        return Page.objects.get(title=self.kwargs['title'].replace('_', ' '))

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'content':self.object.current_revision.content})
        return form_class(**kwargs)

    def form_valid(self, form):
     
        new_revision = PageRevision(content=self.request.POST['content'],
                       revision_summary=self.request.POST['summary'],
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

@login_required
def wiki_section_edit(request, **kwargs):
    header = request.GET['header']
    section = request.GET['name']
    section = re.escape(section)
    # Find the associate wiki and its most current content. 
    page = Page.objects.get(title=kwargs['title'])

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
        section_content = request.POST['content']
        header_level = header[1]
        pattern = re.compile(u'(^|\r\n)(#{'+header_level+u'}\s*'+section+ '(.|\n)*?)(\r\n#{'+header_level+u'}[^#]|$)')
        match = re.search(pattern, page_content)
        revised_page_content = re.sub(pattern, match.group(1) +section_content + match.group(4), page_content)
        new_revision = PageRevision(content=revised_page_content,
                       revision_summary=request.POST['summary'], 
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
            return render(self.request, 'wiki/wiki_not_found.html',{'title':self.kwargs['title']})
        else:
            return super(WikiDetails, self).dispatch(*args, **kwargs)

    def get_object(self):
        return Page.objects.get(title=self.kwargs['title'].replace('_', ' '))



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
        context['comment_list'] = self.object.comments.all()
        return context
        
class WikiCommentAdd(CreateView):
    model = PageComment
    template_name = "wiki/wiki_comment_edit.html"
    
    @method_decorator(login_required)
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

    model = PageComment
    template_name = "wiki/wiki_comment_edit.html"
    fields = ['status','issue','detail']
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WikiCommentEdit, self).dispatch(*args, **kwargs)

class UserPageView(ListView):
    template_name = "wiki/wiki_userpage.html"
    context_object_name = "userpage_list"
    
    def get_queryset(self):
        return UserPage.objects.filter(page__title=self.kwargs['title'].replace('_', ' ')).order_by('-added')
        
    def get_context_data(self):
        context = super(UserPageView, self).get_context_data()
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

