from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone

#from .forms import WikiForm
from .models import Page, PageRevision
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
    def form_valid(self, form):
        new_revision = PageRevision(content=self.request.POST['content'], 
                       revision_summary=self.request.POST['summary'], page=self.object)
        new_revision.save()
        self.object.current_revision=new_revision
        self.object.save()
        return super(WikiEdit, self).form_valid(form)
        
class WikiDetails(DetailView): 
    template_name = "wiki/wiki_detail.html"
    model = Page
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
        return PageRevision.objects.filter(page = self.kwargs['pk']).order_by('-modified_date')

class WikiDiff(DetailView):
    model = PageRevision
    template_name = "wiki/wiki_diff.html"
    

