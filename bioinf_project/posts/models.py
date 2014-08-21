#django core modules
from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericRelation 
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import F

from utils.models import View
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
        return "reply_to_"+self.post.mainpost.title+"_revision_"+str(self.revision_number)

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
    author = models.ForeignKey(User,blank=False,null=False)
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

    #add status of the post

    tags = models.ManyToManyField("tags.Tag",blank=True, related_name="posts")

    title = models.CharField(max_length=255,null=False)

    current_revision = models.OneToOneField('MainPostRevision', blank=True, null=True, verbose_name=_('current revision'))
    # views for the post
    view_count = models.IntegerField(default=0)

    reply_count = models.IntegerField(default=0)

    bookmark_count = models.IntegerField(default=0)

    mainpost_votes = GenericRelation("utils.Vote")

    post_views = GenericRelation("utils.View")

    accepted_answer = models.ForeignKey("ReplyPost", blank=True, null=True, related_name="accepted_root")
    main_post_comments = GenericRelation("utils.Comment")
        ### potential useful fields: watched

    def __unicode__(self):
        return self.title

    @staticmethod
    def update_post_views(post, request, minutes=60):
        "Views are updated per user session"

        # Extract the IP number from the request.
        ip1 = request.META.get('REMOTE_ADDR', '')
        ip2 = request.META.get('HTTP_X_FORWARDED_FOR', '').split(",")[0].strip()
        # 'localhost' is not a valid ip address.
        ip1 = '' if ip1.lower() == 'localhost' else ip1
        ip2 = '' if ip2.lower() == 'localhost' else ip2
        ip = ip1 or ip2 or '0.0.0.0'

        now = timezone.now()
        since = now - timezone.timedelta(minutes=minutes)

        obj_type = ContentType.objects.get_for_model(post)
        obj_id =post.id

        # One view per time interval from each IP address.
        if not post.post_views.filter(ip=ip, date__gt=since):
            new_view = View(ip=ip, content_object=post, date=now)
            new_view.save()
            MainPost.objects.filter(id=post.id).update(view_count=F('view_count') + 1)
        return post


    @staticmethod
    def reset_reply_count():
        for post in MainPost.objects.all():
            print post, post.replies.count()
            post.reply_count = post.replies.count()
            post.save()


    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs = {'pk': self.pk})

    def get_vote_count(self):
        return self.mainpost_votes.filter(choice=1).count() - self.mainpost_votes.filter(choice=-1).count()

    def get_comments(self):
        return self.main_post_comments.all()

class ReplyPost(AbstractPost):
    mainpost = models.ForeignKey(MainPost, related_name = "replies", null=False)
    current_revision = models.OneToOneField('ReplyPostRevision', blank=True, null=True, verbose_name=_('current revision'))
    best_answer = models.BooleanField(default=False)

    reply_post_comments = GenericRelation("utils.Comment")

    replypost_votes = GenericRelation("utils.Vote")

    def __unicode__(self):
        return "reply to:" + self.mainpost.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs = {'pk': self.mainpost.pk})

    def get_vote_count(self):
        return self.replypost_votes.filter(choice=1).count() - self.replypost_votes.filter(choice=-1).count()

    def get_comments(self):
        return self.reply_post_comments.all()



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
        
