from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse 
from django.http import HttpResponseRedirect, HttpResponse, Http404

from wiki.models import Page, PageComment
from tags.models import Tag

from tags.forms import TagForm , WorkflowTagForm
# Create your views here.

#create a moderator mixin
class ModeratorRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous():
            raise Http404("Anonymous user is prohibited")
        elif self.request.user.is_moderator == False:
            raise Http404("Only moderators are permitted")
        else:
            return super(ModeratorRequiredMixin, self).dispatch(*args, **kwargs)
            
            
            
# moderate portal
class ModeratePortal(ModeratorRequiredMixin, TemplateView):

    template_name = "moderate/moderate_main.html"
    
    def get_context_data(self, **kwargs):
        context = super(ModeratePortal, self).get_context_data(**kwargs)
        context['moderate'] = True
        return context
        
# moderate wiki list
class ModerateWikiList(ModeratorRequiredMixin, ListView):
    model = Page
    context_object_name = "wiki_list"
    template_name = "moderate/wiki_moderate_list.html"
    
    def get_queryset(self):
        return Page.objects.order_by('-pending_comment_count')
    
    def get_context_data(self, **kwargs):
        context = super(ModerateWikiList, self).get_context_data(**kwargs)
        context['moderate'] = True
        return context
    
class ModerateWiki(ModeratorRequiredMixin, DetailView):
    model = Page
    template_name = "moderate/wiki_moderate.html"
    
    def get_object(self):
        return Page.objects.get(title=self.kwargs['title'].replace('_', ' '))
        
    def get_context_data(self, **kwargs):
        context = super(ModerateWiki, self).get_context_data(**kwargs)
        context['moderate'] = True
        context['pending_comments'] = self.object.comments.order_by('-modified').filter(status = 1)
        return context
        
class ChangeWikiStatus(ModeratorRequiredMixin, UpdateView): 
    model = Page
    fields = ['status']

    def get_object(self):
        return Page.objects.get(title=self.kwargs['title'].replace('_', ' '))
        
    def get_success_url(self):
        return reverse('moderate:wiki', kwargs={'title':self.object.get_title()})

class ChangeWikiCommentStatus(ModeratorRequiredMixin, UpdateView): 
    model = PageComment
    fields = ['status']
    
    def get_success_url(self):
        return reverse('moderate:wiki', kwargs={'title':self.object.page.get_title()})
        
        
        
class ModerateTagList(ModeratorRequiredMixin, ListView):
    model = Tag
    context_object_name = "tag_list"
    template_name = "moderate/tag_moderate_list.html"
    
    def get_queryset(self):
        return Tag.objects.order_by('-count')
    
    def get_context_data(self, **kwargs):
        context = super(ModerateTagList, self).get_context_data(**kwargs)
        context['moderate'] = True
        return context
        
class ModerateTag(ModeratorRequiredMixin, UpdateView):
    model = Tag
    template_name = "moderate/tag_moderate.html"
    fields = ['name', 'icon','wiki_page', 'parent', 'status', 'categories']
    def get_object(self):
        return Tag.objects.get(name=self.kwargs['name'].replace('_', ' '))
        
    def get_form_class(self):
        if self.object.get_categories_display() == "workflow":
            return WorkflowTagForm
        else: 
            return TagForm
            
    def form_valid(self, form):
        image_field = form.cleaned_data.get('icon')
        if image_field:
            image_file = StringIO.StringIO(image_field.read())
            image = Image.open(image_file)
            SIZE = 40,40
            image = image.resize(SIZE, Image.ANTIALIAS)
            image_file = StringIO.StringIO()
            image.save(image_file, 'JPEG', quality=90)
            image_field.file = image_file
        return super(TagEdit,self).form_valid(form)
        
        
    def get_context_data(self, **kwargs):
        context = super(ModerateTag, self).get_context_data(**kwargs)
        context['moderate'] = True
        return context
        
        
class ChangeTagStatus(ModeratorRequiredMixin, UpdateView): 
    model = Tag
    fields = ['status']

    def get_object(self):
        return Tag.objects.get(name=self.kwargs['name'].replace('_', ' '))
        
    def get_success_url(self):
        return reverse('moderate:tag-list')