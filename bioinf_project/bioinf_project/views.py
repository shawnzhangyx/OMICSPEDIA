from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render

from tags.models import Tag
from wiki.models import Page
from posts.models import MainPost
class IndexView(TemplateView):
    template_name = "index.html"


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
