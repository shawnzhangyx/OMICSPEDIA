import re
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from utils import diff_match_patch
#from .forms import WikiForm
from .models import Page, PageRevision, PageComment
import markdown
# Create your views here.


class IndexView(ListView): 
    model = Page 
    template_name = "wiki/index.html"
    context_object_name = "wiki_list"
    
class WikiNew(CreateView): 
    template_name = "wiki/wiki_new.html"
    model = Page
    fields = ['title', 'tags']
    def form_valid(self, form):
        form.save()
        new_revision = PageRevision(content=self.request.POST['content'], 
                       revision_summary=self.request.POST['summary'], 
                       page=form.instance, author=self.request.user)
        new_revision.save()
        form.instance.current_revision=new_revision
        return super(WikiNew, self).form_valid(form)

    
class WikiEdit(UpdateView): 
    model = Page
   # fields = '__all__'
    fields = ['title', 'tags']
    template_name = 'wiki/wiki_edit.html'

    def get_object(self):
        return Page.objects.get(title=self.kwargs['title'].replace('_', ' '))

    def form_valid(self, form):
        if self.request.POST['submit']=='Preview':
            self.request.session['preview'] = self.request.POST['content']
            return HttpResponseRedirect(reverse("wiki:wiki-edit", args={self.object.get_title()}))
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

    def get_queryset(self):
        return PageRevision.objects.filter(page__title = self.kwargs['title']).order_by('-modified_date')

    def get_context_data(self, **kwargs):
        context = super(WikiHistory, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(title = self.kwargs['title'])
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
    
    def get_form_kwargs(self):
        kwargs = super(WikiCommentAdd, self).get_form_kwargs()
        page = Page.objects.get(title=self.kwargs['title'])
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
