from django.views.generic import TemplateView, ListView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from datetime import datetime, timedelta

from tags.models import Tag
from wiki.models import Page
from posts.models import MainPost


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        posts = MainPost.objects.filter(created__gte=datetime.today() - timedelta(days=30)).order_by('-vote_count')
        context['post_list'] = posts
        return context

def search(request):
#    template_name = "search.html"
    field = request.GET['search_field']
    text = request.GET['search_text']
    wiki = ''
    posts = ''
#    if field == "All" or field == "Tag":
#        tags = Tag.objects.filter(name__icontains = text)#.exclude(parent__isnull=False)
    if field == "All" or field == "Wiki":
        wiki = Page.objects.filter(title__icontains = text)
    if field == "All" or field == "Post":
        posts = MainPost.objects.filter(title__icontains = text)
    return render(request, "search_results.html", {"wiki_list":wiki,"post_list":posts,"search_text":text})


class PortalView(ListView):
    template_name = 'omics_portal.html'

    def get_queryset(self):
        if self.kwargs['name'] =='':
            return Tag.objects.filter(parent__isnull=True, categories=1)
        else:
            return Tag.objects.filter(parent__name=self.kwargs['name'])

    def get_context_data(self, **kwargs):
        context = super(PortalView, self).get_context_data(**kwargs)
        try:
            category = Tag.objects.get(name = self.kwargs['name'])
        except Tag.DoesNotExist:
            pass # Root
        else:
            context['category'] = category
        return context

def portal_tag(request):
    context = RequestContext(request)
    if request.method == "GET":
        tag_name = request.GET['tag_name']
        tag = Tag.objects.get(name = tag_name)
        software_list = tag.pages.filter(software__isnull=False)
        usertag_list = tag.usertags.filter(answer_count__gt = 0)
        return render_to_response('utils/portal_tag.html', {'tag': tag,'software_list':software_list,'usertag_list':usertag_list}, context)

def help_page_view(request,**kwargs):
    context = RequestContext(request)
    help_html = 'help/'+kwargs['help_page']+'.html'
    return render_to_response(help_html,context)

