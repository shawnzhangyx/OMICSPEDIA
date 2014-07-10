#django core modules
from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.core.urlresolvers import reverse

#local apps
from tags.models import Tag

# Create your models here.

# --------------- #
# Can have an abstract Post class and two differen children: MainPost and Answers #
# For now, we just follow the Biostar standard. #
# comment functions would be added later
class AbstractPost(models.Model):
    #---- model fields ----#
    content = models.TextField(default='Enter here')
    vote_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag,blank=True,)
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    #---- functions ----#
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id: 
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(AbstractPost, self).save(*args, **kwargs)

    class Meta:
        abstract = True



class MainPost(AbstractPost):
    def __unicode__(self):
        return self.title
    title = models.CharField(max_length=255,null=False)
    answered = models.BooleanField(default=False)
        
    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs = {'pk': self.pk})
    ### potential useful fields: 

class ReplyPost(AbstractPost):
    root = models.ForeignKey(MainPost, related_name = "replies")
   
class MainPostForm(ModelForm):
    class Meta: 
        model = MainPost
        #fields = '__all__'
        fields = ['title', 'content','tags']
#    def save(self):
#        post = super(PostForm, self).save(commit=False)
#        post.creation_date = timezone.now()
#        post.last_modified_date = timezone.now()
#        post.save()
#        self.save_m2m()
#        return 

class ReplyPostForm(ModelForm): 
    class Meta: 
        model = ReplyPost
        fields = ['content','tags']
