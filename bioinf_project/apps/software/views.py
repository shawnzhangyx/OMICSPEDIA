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
    paginate_by = 20

    def get_queryset(self):
        tab = self.request.GET.get('tab')
        if self.kwargs['tag'] !='root':
            tag = Tag.objects.get(name=self.kwargs['tag'])
            if tab == "Votes" or not tab:
                return Tool.objects.filter(page__tags__in = [tag]).order_by('-vote_count')
            elif tab == "Bugs":
                return Tool.objects.filter(page__tags__in = [tag]).order_by('-bug_count')
        else:
            return Tool.objects.none()
            
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)    
        if self.kwargs['tag'] =='root':
            tags = Tag.objects.filter(categories=1, parent__isnull=True).order_by('-tool_count')
        else: 
            parent = Tag.objects.get(name=self.kwargs['tag'])
            tags = parent.children.all().order_by('-tool_count')
            context['parent'] = parent
        context['tag_list'] = tags
        context['software_count'] = Tool.objects.all().count()
        context['tab'] = self.request.GET.get('tab') or 'Votes'
        return context
    
class SoftwareListView(ListView):
    model = Tool
    template_name = "software/software_list.html"
    context_object_name = "software_list"
    paginate_by = 20
    
    def get_queryset(self): 
        tab = self.request.GET.get('tab') or 'Vote'
        dict = {'Vote':'-vote_count',}
        return Tool.objects.all().order_by(dict[tab])
    
    def get_context_data(self, **kwargs):
        context = super(SoftwareListView, self).get_context_data(**kwargs)
        context['tab'] = self.request.GET.get('tab') or 'Vote'
        return context
    
    
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

