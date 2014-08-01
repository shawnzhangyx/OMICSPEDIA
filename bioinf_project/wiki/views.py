from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from utils import diff_match_patch
#from .forms import WikiForm
from .models import Page, PageRevision
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
                       revision_summary=self.request.POST['summary'], page=form.instance)
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
                       revision_summary=self.request.POST['summary'], page=self.object)
        new_revision.save()
        self.object.current_revision=new_revision
        self.object.save()
        return super(WikiEdit, self).form_valid(form)
        
    def get_context_data(self, **kwargs):
       context = super(WikiEdit, self).get_context_data(**kwargs)
       if 'preview' in self.request.session:
           context['preview'] = markdown.markdown(self.request.session['preview'],extensions=['codehilite'])
           #context['form'].initial['content'] = self.request.session['preview']
           context['content'] = self.request.session['preview']
           del self.request.session['preview']
       return context

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
        return context
    

