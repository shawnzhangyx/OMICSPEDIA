from django.shortcuts import render
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from .models import Comment
from wiki.models import Page
from posts.models import MainPost, ReplyPost
# Create your views here.

class CommentNew(CreateView):
    template_name = "wiki/comment_new.html"
    model = Comment
    fields = ['content']
    def form_valid(self, form):
        # can write a more compact function. 

        if self.kwargs['comment_on'] == 'wiki':
            target = Page.objects.get(pk=self.kwargs['pk'])
        elif self.kwargs['comment_on'] == 'posts':
            target = MainPost.objects.get(pk=self.kwargs['pk'])
        elif self.kwargs['comment_on'] == 'replyposts':
            target = ReplyPost.objects.get(pk=self.kwargs['pk'])

        form.instance = Comment(content_object=target, content = self.request.POST['content'])
        return super(CommentNew, self).form_valid(form)

    def get_success_url(self):
        if self.kwargs['comment_on'] == "wiki":
            return reverse('wiki:wiki-detail',kwargs={'pk':self.kwargs['pk']}) 
        elif self.kwargs['comment_on'] == "posts":
            return reverse('posts:post-detail', kwargs={'pk':self.kwargs['pk']})
        elif self.kwargs['comment_on'] == "replyposts":
            return reverse('posts:post-detail', kwargs={'pk':ReplyPost.objects.get(pk=self.kwargs['pk']).mainpost.pk })
