from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone

#from .forms import WikiForm
from .models import Page, PageForm
# Create your views here.


class IndexView(ListView): 
    model = Page 
    template_name = "wiki/index.html"
    context_object_name = "wiki_list"
    
class WikiNew(FormView): 
    template_name = "wiki/wiki_new.html"
    form_class = PageForm
    success_url = '/wiki/'
    def form_valid(self, form):
        form.save()
        return super(WikiNew, self).form_valid(form)
    # success_url = reverse("wiki:wiki-detail",args=(wiki_id,))

    
class WikiEdit(UpdateView): 
    model = Page
    fields = ['title', 'content','tags']
    template_name = 'wiki/wiki_edit.html'
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.last_modified_date = timezone.now()
        instance.save()
        return super(WikiEdit, self).form_valid(form)
class WikiDetails(DetailView): 
    template_name = "wiki/wiki_detail.html"
    model = Page
    #need to display everything in the same subject. 
