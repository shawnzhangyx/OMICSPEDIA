from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Tag
from posts.models import MainPost
from wiki.models import Page, PageRevision
# Create your views here.

class TagList(ListView):
#    model = Tag
    template_name = "tags/index.html"
    queryset = Tag.objects.filter(parent__isnull=True)

class TagCreate(CreateView):
    model = Tag
    template_name = "tags/tag_create.html"
    fields = ['name']
    def form_valid(self, form):
        # if a wiki with the same tag name exists, associate this tag with the existing wiki. 
        try: 
            old_page = Page.objects.get(title = form.instance.name)
        except Page.DoesNotExist:
            pass # create an entirely new tag
        else: 
            # create a tag using old wiki.
            new_tag = Tag(pk=old_page.pk, name=old_page.title, title=old_page.title)
                          #comments=old_page.comments, current_revision=old_page.current_revision)
            if int(self.kwargs['parent_id'])>0:
                new_tag.parent = Tag.objects.get(pk= self.kwargs['parent_id'])
            new_tag.save()
            return HttpResponseRedirect(reverse('tags:tag-detail',kwargs={'pk':new_tag.pk}))
            #return HttpResponseRedirect( reverse('tags:tag-index'))
        #super(TagCreate, self).form_invalid(form) # should provide an error message that this tag already exist. 
        form.instance.title = form.instance.name
        if int(self.kwargs['parent_id'])>0:
            form.instance.parent = Tag.objects.get(pk= self.kwargs['parent_id'])
        form.save()
       # if self.request.POST: 
        new_revision = PageRevision(#content=self.request.POST['content'], 
                                    #revision_summary=self.request.POST['summary'], 
                                    page=form.instance)
        new_revision.save()
        form.instance.current_revision=new_revision
        form.instance.tags.add(form.instance)
        return super(TagCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TagCreate,self).get_context_data(**kwargs)
        if int(self.kwargs['parent_id'])>0:
            tag = Tag.objects.get(pk= self.kwargs['parent_id'])
            message = ""
            while tag: 
                message = tag.name+'/' + message
                tag = tag.parent
            message = "This tag will be created under: " + message
        else: 
            message = '''Tips: if you want to create a new tag nested under another tags,
                       please do that in the respective tag page.'''
        context['message'] = message

        return context

class TagDetails(DetailView):
    template_name = 'tags/tag_detail.html'
    model = Tag
    def get_context_data(self, **kwargs):
        context = super(TagDetails, self).get_context_data(**kwargs)
        context['post_list'] = MainPost.objects.filter(tags = self.object.id)
        context['wiki_list'] = self.object.page_set.all()
        return context
 
class TagDelete(DeleteView):
    model = Tag
    template_name = 'tags/tag_delete.html'
    success_url = reverse_lazy('tags:tag-index')

class TagSearch(ListView):
    template_name = 'tags/tag_search_results.html'
    
    #def dispatch(self, request, *args, **kwargs):

    def get_queryset(self):
        return Tag.objects.filter(name__icontains = self.request.GET['search_content'])#.exclude(parent__isnull=False)
    
    def get_context_data(self, **kwargs):
        context = super(TagSearch, self).get_context_data(**kwargs)
        context['pre_search_content'] = self.request.GET['search_content']
        return context
