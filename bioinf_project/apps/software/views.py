from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import render
#from .forms import WikiForm
from .models import Tool
from .forms import ToolForm
# Create your views here.


class IndexView(ListView):
    model = Tool
    template_name = "software/index.html"
    context_object_name = "software_list"
    
class SoftwareNew(CreateView):
    form_class = ToolForm
    template_name = "software/software_edit.html"

class SoftwareEditView(UpdateView):
    #model = Tool
    form_class = ToolForm
    template_name = "software/software_edit.html"

    def get_object(self):
        return Tool.objects.get(name=self.kwargs['name'])

class SoftwareDetailView(DetailView):
    model = Tool
    template_name = "software/software_detail.html"

    def get_object(self, **kwargs):
        return Tool.objects.get(name=self.kwargs['name'])

def software_precreate_view(request):
    return render(request, "software/software_pre_create.html")

