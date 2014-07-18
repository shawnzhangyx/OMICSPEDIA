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

class PostRevision(models.Model):
    revision_number = models.IntegerField(_('revision number'), editable=False)
    revision_summary = models.TextField(_('revision summary'), blank=True)
    # editor = models.ForeignKey(User, blank=True, null = True)
    content = models.TextField(blank=True, verbose_name = _("page content"))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_("modified date"))

    
    def __unicode__(self):
        return self.page.title+"_revision_"+str(self.revision_number)

    def save(self, *args, **kwargs):
        if not self.revision_number: 
            try: 
                previous_revision = self.page.pagerevision_set.latest()
                self.revision_number = previous_revision.revision_number + 1
            except PageRevision.DoesNotExist:
                self.revision_number = 1
        super(PageRevision, self).save(*args, **kwargs)


class AbstractPost(models.Model):
    #---- model fields ----#
    content = models.TextField(default='Enter here')
    vote_count = models.IntegerField(default=0)
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    #---- functions ----#
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id: 
            self.created = timezone.now()
        self.last_modified = timezone.now()
        return super(AbstractPost, self).save(*args, **kwargs)

    class Meta:
        abstract = True



class MainPost(AbstractPost):
    tags = models.ManyToManyField(Tag,blank=True,)
    title = models.CharField(max_length=255,null=False)
    answered = models.BooleanField(default=False)
        
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs = {'pk': self.pk})
    ### potential useful fields: 

class ReplyPost(AbstractPost):
    root = models.ForeignKey(MainPost, related_name = "replies", null=False)
    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs = {'pk': self.root.pk})

class MainPostForm(ModelForm):
    class Meta: 
        model = MainPost
        #fields = '__all__'
        fields = ['title', 'content','tags']

class ReplyPostForm(ModelForm): 
    class Meta: 
        model = ReplyPost
        fields = ['content','tags']
