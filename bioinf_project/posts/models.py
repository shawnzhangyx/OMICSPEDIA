#django core modules
from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

#local apps
from tags.models import Tag

# Create your models here.

# --------------- #
# Can have an abstract Post class and two differen children: MainPost and Answers #
# For now, we just follow the Biostar standard. #
# comment does not have revision history. 

class AbstractPostRevision(models.Model):
    revision_number = models.IntegerField(_('revision number'), editable=False)
    revision_summary = models.TextField(_('revision summary'), blank=True)
    # editor = models.ForeignKey(User, blank=True, null = True)
    content = models.TextField(blank=True, verbose_name = _("post content"))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_("modified date"))
    class Meta:
        abstract = True
        get_latest_by= 'revision_number'    
        
class MainPostRevision(AbstractPostRevision):
    post = models.ForeignKey("MainPost", on_delete = models.CASCADE, verbose_name=_("post"))

    def __unicode__(self):
        return self.post.title+"_revision_"+str(self.revision_number)
        
    def save(self, *args, **kwargs):
        if not self.revision_number: 
            try: 
                previous_revision = self.post.mainpostrevision_set.latest()
                self.revision_number = previous_revision.revision_number + 1
            except MainPostRevision.DoesNotExist:
                self.revision_number = 1
        super(MainPostRevision, self).save(*args, **kwargs)
    def get_pre_revision(self):
        try: 
            return MainPostRevision.objects.get(revision_number = self.revision_number - 1, page = self.page)
        except IndexError:
            return
            
class ReplyPostRevision(AbstractPostRevision):
    post = models.ForeignKey("ReplyPost", on_delete = models.CASCADE, verbose_name=_("post"))

    def __unicode__(self):
        return self.post.title+"_revision_"+str(self.revision_number)

    def save(self, *args, **kwargs):
        if not self.revision_number: 
            try: 
                previous_revision = self.post.replypostrevision_set.latest()
                self.revision_number = previous_revision.revision_number + 1
            except ReplyPostRevision.DoesNotExist:
                self.revision_number = 1
        super(ReplyPostRevision, self).save(*args, **kwargs)

    def get_pre_revision(self):
        try: 
            return ReplyPostRevision.objects.get(revision_number = self.revision_number - 1, page = self.page)
        except IndexError:
            return

            
class AbstractPost(models.Model):
    #---- model fields ----#
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
    current_revision = models.OneToOneField('MainPostRevision', blank=True, null=True, verbose_name=_('current revision'))
    answered = models.BooleanField(default=False)
        ### potential useful fields: watched 
        
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs = {'pk': self.pk})


class ReplyPost(AbstractPost):
    mainpost = models.ForeignKey(MainPost, related_name = "replies", null=False)
    current_revision = models.OneToOneField('ReplyPostRevision', blank=True, null=True, verbose_name=_('current revision'))
    best_answer = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "reply to:" + self.mainpost.title
    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs = {'pk': self.mainpost.pk})

# comments have no revision history, and allow minimum makeup. 
class AbstractComment(models.Model):
    content = models.TextField(max_length=600, null=False)
    last_modified = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.last_modified = timezone.now()
        return super(AbstractPost, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True
        
class MainPostComment(AbstractComment):
    post = models.ForeignKey(MainPost, related_name = "comments", verbose_name = _("main post comment"))
    
    
class ReplyPostComment(AbstractComment):
    post = models.ForeignKey(ReplyPost, related_name = "comments", verbose_name = _("reply post comment"))    
        
#class MainPostForm(ModelForm):
#    class Meta: 
#        model = MainPost
#        #fields = '__all__'
#        fields = ['title','tags']

#class ReplyPostForm(ModelForm): 
#    class Meta: 
#        model = ReplyPost
#        fields = ['tags']
