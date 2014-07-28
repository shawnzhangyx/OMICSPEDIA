from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone

#from .forms import WikiForm
from .models import Tool, ToolForm 
# Create your views here.


class IndexView(ListView): 
    model = Tool
    template_name = "tool_wiki/index.html"
    context_object_name = "tool_list"
    
class ToolNew(FormView): 
    template_name = "tool_wiki/tool_new.html"
    form_class = ToolForm
    success_url = '/tools/'
    def form_valid(self, form):
        form.save()
        return super(ToolNew, self).form_valid(form)
    # success_url = reverse("wiki:wiki-detail",args=(wiki_id,))

    
class ToolEdit(UpdateView): 
    model = Tool
    fields = ['title', 'content','tags']
    template_name = 'tool_wiki/tool_edit.html'
    def form_valid(self, form):
        return super(WikiEdit, self).form_valid(form)

class ToolDetails(DetailView): 
    template_name = "tool_wiki/tool_detail.html"
    model = Tool
    #need to display everything in the same subject. 

