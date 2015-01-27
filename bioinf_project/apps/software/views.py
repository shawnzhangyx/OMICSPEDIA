from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import render
#from .forms import WikiForm
from .models import Tool
from tags.models import Tag
from .forms import ToolForm, ToolNewForm
# Create your views here.


class IndexView(ListView):
    model = Tool
    template_name = 'software/index.html'
    context_object_name = "software_list"
    
    def get_queryset(self):
        if self.kwargs['tag'] !='root':
            tag = Tag.objects.get(name=self.kwargs['tag'])
            return Tool.objects.filter(page__tags__in = [tag])
        else:
            return 
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        if self.kwargs['tag'] =='root':
            tags = Tag.objects.filter(categories=1, parent__isnull=True)
        else: 
            parent = Tag.objects.get(name=self.kwargs['tag'])
            tags = parent.children.all()
            context['parent'] = parent
        context['tag_list'] = tags
        context['software_count'] = Tool.objects.all().count()
        
        return context
    
class SoftwareListView(ListView):
    model = Tool
    template_name = "software/software_list.html"
    context_object_name = "software_list"
    
class SoftwareNew(CreateView):
    form_class = ToolNewForm
    template_name = "software/software_edit.html"
        
    def form_valid(self, form):
        form.instance = Tool.create(form.instance.name, self.request.user)
        return super(SoftwareNew, self).form_valid(form)
        
    def get_success_url(self):
        return reverse('software:software-edit', kwargs={'name':self.object.name})
    
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
    
    def get_context_data(self, **kwargs):
        context = super(SoftwareDetailView, self).get_context_data(**kwargs)
        if hasattr(self.object.page, 'wiki_tag'):
            context['usertag_list'] = self.object.page.wiki_tag.usertags.filter(answer_count__gt = 0)
        return context

