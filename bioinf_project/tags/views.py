from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView
# Create your views here.
from .models import Tag

def index_view(request):
    tag_list = Tag.objects.all()
    context_dict = {'tag_list':tag_list}
    if request.method =="POST": 
        new_tag_name = request.POST['tag_name']
        if new_tag_name =='':
            context_dict['error_message']='You did not put in anything'
            return render(request, 'tags/index.html', context_dict)
        else:
            try: 
                Tag.objects.get(name__exact = new_tag_name)
            except(Tag.DoesNotExist): 
                new_tag = Tag(name=new_tag_name)
                new_tag.save()
                return HttpResponseRedirect(reverse('tags:tag-index'))
            else:
                context_dict['error_message']='tag already existed'
                return render(request, 'tags/index.html', context_dict)
    else: 
        return render(request, 'tags/index.html', context_dict)

class TagDetails(DetailView):
    template_name = 'tags/tag_detail.html'
    model = Tag
