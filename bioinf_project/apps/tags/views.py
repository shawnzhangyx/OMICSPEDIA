from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from utils import pagination
import StringIO
from PIL import Image

from .models import Tag, UserTag
from posts.models import MainPost
from wiki.models import Page, PageRevision
from .forms import TagForm, TagCreateForm, WorkflowTagForm
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

# Create your views here.

class TagList(ListView):
#    model = Tag
    template_name = "tags/index.html"
    paginate_by = 50
    
    def get_queryset(self):
        type = self.request.GET.get('type')
        if type:
            return Tag.objects.filter(categories = type).order_by('-count')
        return Tag.objects.order_by('-count')#filter(parent__isnull=True)


class TagCreate(CreateView):
    form_class = TagCreateForm
    template_name = "tags/tag_create.html"

    @method_decorator(permission_required("tags.add_tag",login_url="/accounts/email-verification/"))
    def dispatch(self, *args, **kwargs):
        return super(TagCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'categories':0})
        return form_class(**kwargs)

    def form_valid(self, form):
        form.instance = Tag.create(form.instance.name, form.instance.categories, form.instance.icon, self.request.user)
        if self.kwargs['parent_name']!='':
            parent = Tag.objects.get(name = self.kwargs['parent_name'])
            form.instance.parent = parent
            form.save()
        return super(TagCreate, self).form_valid(form)
    
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
            message = '''Tips: Each tag should associate with a wiki page. So before creating a tag, find or create a wiki page with the same name.'''
        context['message'] = message
        return context


class TagEdit(UpdateView):
    #form_class = TagForm
    template_name = "tags/tag_edit.html"

    @method_decorator(permission_required("tags.change_tag",login_url="/accounts/email-verification/"))
    def dispatch(self, *args, **kwargs):
        return super(TagEdit, self).dispatch(*args, **kwargs)
        
    def get_object(self):
        return Tag.objects.get(name=self.kwargs['name'].replace('_',' '))

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
        
class TagDetails(DetailView):
    template_name = 'tags/tag_detail.html'
    model = Tag
    
    def get_object(self):
        return Tag.objects.get(name=self.kwargs['name'])
        
    def get_context_data(self, **kwargs):
        page_limit = 5
        context = super(TagDetails, self).get_context_data(**kwargs)
        tab = self.request.GET.get('tab')
        if not tab:
            tab = 'Summary'
        page = self.request.GET.get('page')
        # lists that are paginated. 
        wiki_list = self.object.pages.all()
        question_list = self.object.questions()
        discussion_list = self.object.discussions()
        blog_list = self.object.blogs()
        usertag_list = self.object.usertags.filter(answer_count__gt = 0).order_by('-answer_count')
        # get the count 
        wiki_list_count = wiki_list.count()
        question_list_count = question_list.count()
        discussion_list_count = discussion_list.count()
        blog_list_count = blog_list.count()
        usertag_list_count = usertag_list.count()
        
        # paginate the list 
        wiki_list = pagination(wiki_list,page,page_limit)
        question_list = pagination(question_list,page,page_limit)
        discussion_list = pagination(discussion_list,page,page_limit)
        blog_list = pagination(blog_list,page,page_limit)
        usertag_list = pagination(usertag_list,page,page_limit)
        # 
        
        
        context['tab'] = tab
        context['tag_wiki'] = self.object.wiki_page
        context['wiki_list'] = wiki_list#self.object.pages.all()
        context['question_list'] = question_list #self.object.questions()
        context['discussion_list'] = discussion_list #self.object.discussions()
        context['blog_list'] = blog_list #self.object.blogs()
        context['usertag_list'] = usertag_list #self.object.usertags.filter(answer_count__gt = 0).order_by('-answer_count')
        # list count 
        context['wiki_list_count'] = wiki_list_count 
        context['question_list_count'] = question_list_count 
        context['discussion_list_count'] = discussion_list_count 
        context['blog_list_count'] = blog_list_count 
        context['usertag_list_count'] = usertag_list_count 
        # for workflow tags: 
        #if self.object.get_categories_display == "workflow":
        software_list = self.object.pages.filter(software__isnull=False)
        software_list_count = software_list.count()
        software_list = pagination(software_list, page, page_limit)
        context['software_list'] = software_list
        context['software_list_count'] = software_list_count
        # pagination object. 
        tab_list_dict = {'Wiki':wiki_list,'Software':software_list, 'Questions':question_list, 'Discussions':discussion_list, 'Blogs':blog_list, 'Contributors':usertag_list, 'Summary':False,'':False}
        page_obj = tab_list_dict[tab]
        context['page_obj'] = page_obj 

        if page_obj != False:
            context['is_paginated']=True
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
            contains = request.GET.get('suggestion')
    suggest_tag_list = Tag.objects.get_tag_search_list(0, contains)
    return render_to_response('tags/tag_suggest_list.html', {'suggest_tag_list': suggest_tag_list, 'suggest':contains }, context)
