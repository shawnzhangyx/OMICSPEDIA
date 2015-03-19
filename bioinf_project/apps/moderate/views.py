from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse 

from wiki.models import Page, PageComment
# Create your views here.

# moderate portal
class ModeratePortal(TemplateView):
    template_name = "moderate/moderate_main.html"
    
    
# moderate wiki list
class ModerateWikiList(ListView):
    model = Page
    context_object_name = "wiki_list"
    template_name = "moderate/wiki_moderate_list.html"
    #   paginate_by = 50
    
    def get_context_data(self, **kwargs):
        context = super(ModerateWikiList, self).get_context_data(**kwargs)
        context['moderate'] = True
        return context
    
class ModerateWiki(DetailView):
    model = Page
    template_name = "moderate/wiki_moderate.html"
    
    def get_object(self):
        return Page.objects.get(title=self.kwargs['title'].replace('_', ' '))
        
    def get_context_data(self, **kwargs):
        context = super(ModerateWiki, self).get_context_data(**kwargs)
        context['moderate'] = True
        context['pending_comments'] = self.object.comments.order_by('-modified').filter(status = 1)
        return context
        
class ChangeWikiCommentStatus(UpdateView): 
    model = PageComment
    fields = ['status']
    
    def get_success_url(self):
        return reverse('moderate:wiki', kwargs={'title':self.object.page.get_title()})