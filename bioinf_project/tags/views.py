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
        if Page.objects.filter(title = form.instance.name):
            return HttpResponseRedirect( reverse('tags:tag-index'))
        #super(TagCreate, self).form_invalid(form) # should provide an error message that this tag already exist. 
        form.instance.title = form.instance.name
        form.save()
       # if self.request.POST: 
        new_revision = PageRevision(content=self.request.POST['content'], 
                       revision_summary=self.request.POST['summary'], page=form.instance)
        new_revision.save()
        form.instance.current_revision=new_revision
        form.instance.tags.add(form.instance)
        return super(TagCreate, self).form_valid(form)

        

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

