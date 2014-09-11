from django.views.generic import TemplateView, ListView
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


class PortalView(ListView):
    template_name = 'omics_portal.html'

    def get_queryset(self):
        if self.kwargs['name'] =='':
            return Tag.objects.filter(parent__isnull=True, categories=2)
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

class HelpView(TemplateView):
    template_name = "help.html"
