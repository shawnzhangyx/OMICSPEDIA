from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Tag, UserTag
from posts.models import MainPost
from wiki.models import Page, PageRevision
from .forms import TagForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class TagList(ListView):
#    model = Tag
    template_name = "tags/index.html"
    paginate_by = 20
    queryset = Tag.objects.filter(parent__isnull=True)


class TagCreate(CreateView):
    form_class = TagForm
    template_name = "tags/tag_create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TagCreate, self).dispatch(*args, **kwargs)

        return form_class(**kwargs)
    def get_context_data(self, **kwargs):
        context = super(TagCreate,self).get_context_data(**kwargs)
        if self.kwargs['parent_name'] !='':
            tag = Tag.objects.get(name = self.kwargs['parent_name'])
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

class TagEdit(UpdateView):
    form_class = TagForm
    template_name = "tags/tag_edit.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TagEdit, self).dispatch(*args, **kwargs)
        
    def get_object(self):
        return Tag.objects.get(name=self.kwargs['name'].replace('_',' '))


class TagDetails(DetailView):
    template_name = 'tags/tag_detail.html'
    model = Tag
    
    def get_object(self):
        return Tag.objects.get(name=self.kwargs['name'])
        
    def get_context_data(self, **kwargs):
        context = super(TagDetails, self).get_context_data(**kwargs)
        tab = self.request.GET.get('tab')
        context['tab'] = tab
        context['tag_wiki'] = self.object.wiki_page
        context['wiki_list'] = self.object.pages.all()
        context['question_list'] = self.object.questions()
        context['discussion_list'] = self.object.discussions()
        context['blog_list'] = self.object.blogs()
        context['usertag_list'] = self.object.usertags.filter(answer_count__gt = 0)
        return context

class TagDelete(DeleteView):
    model = Tag
    template_name = 'tags/tag_delete.html'
    success_url = reverse_lazy('tags:tag-index')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TagDelete, self).dispatch(*args, **kwargs)
        
    def get_object(self):
        return Tag.objects.get(name=self.kwargs['name'])

class TagUserContributionView(ListView):
    
    template_name = 'tags/tag_user_post_list.html'
    
    def get_queryset(self):
        usertag = UserTag.objects.get_or_create(tag__name=self.kwargs['name'], user__user_profile__name=self.kwargs['user'])[0]
        return usertag.answers.all()
    
    def get_context_data(self):
        context = super(TagUserContributionView, self).get_context_data()
        usertag = UserTag.objects.get_or_create(tag__name=self.kwargs['name'], user__user_profile__name=self.kwargs['user'])[0]
        context['usertag'] = usertag
        return context 
    
def suggest_tags(request):
    context = RequestContext(request)
    suggest_tag_list = []
    contains = ''
    if request.method == 'GET':
            contains = request.GET['suggestion']
    suggest_tag_list = Tag.objects.get_tag_search_list(0, contains)
    return render_to_response('tags/tag_suggest_list.html', {'suggest_tag_list': suggest_tag_list, 'suggest':contains }, context)
