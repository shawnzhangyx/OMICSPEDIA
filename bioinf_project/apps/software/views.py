from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone

#from .forms import WikiForm
from .models import Tool
# Create your views here.


class IndexView(ListView):
    model = Tool
    template_name = "software/index.html"
    context_object_name = "software_list"

class SoftwareNew(CreateView):
    model = Tool
    template_name = "software/software_edit.html"

class SoftwareEditView(UpdateView):
    model = Tool
    template_name = "software/software_edit.html"

    def get_object(self):
        return Tool.objects.get(name=self.kwargs['name'])

class SoftwareDetailView(DetailView):
    model = Tool
    template_name = "software/software_detail.html"

    def get_object(self, **kwargs):
        return Tool.objects.get(name=self.kwargs['name'])

