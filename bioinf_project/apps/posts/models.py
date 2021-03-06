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
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from utils.models import View, AbstractBaseRevision

from wiki.models import replace_wikilinks, GetMarkdownMixin
# Create your models here.

# --------------- #
# Can have an abstract Post class and two differen children: MainPost and Answers #
# For now, we just follow the Biostar standard. #
# comment does not have revision history.



class MainPostRevision(GetMarkdownMixin, AbstractBaseRevision):
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
            return MainPostRevision.objects.get(revision_number = self.revision_number - 1, post = self.post)
        except IndexError:
            return
 

class ReplyPostRevision(GetMarkdownMixin, AbstractBaseRevision):
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
            return ReplyPostRevision.objects.get(revision_number = self.revision_number - 1, post = self.post)
        except IndexError:
            return
            

class AbstractPost(models.Model):
    #---- model fields ----#
    vote_count = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,blank=False,null=False)
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    #add status of the post
    OPEN, PROTECTED, DELETED = range(3) 
    STATUS_CHOICE = [(OPEN, "open"), (PROTECTED, "protected"), (DELETED, "deleted")]
    status = models.IntegerField(choices=STATUS_CHOICE, default=OPEN)
    #---- functions ----#
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.last_modified = timezone.now()
        return super(AbstractPost, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class QuestionManager(models.Manager):
    def get_queryset(self):
        return super(QuestionManager, self).get_queryset().filter(type=0)
        
class DiscussionManager(models.Manager):
    def get_queryset(self):
        return super(DiscussionManager, self).get_queryset().filter(type=1)
        
class BlogManager(models.Manager):
    def get_queryset(self):
        return super(BlogManager, self).get_queryset().filter(type=2)
        
        
class MainPost(AbstractPost):

    objects = models.Manager()
    questions = QuestionManager()
    discussions = DiscussionManager()
    blogs = BlogManager()
    
    tags = models.ManyToManyField("tags.Tag",blank=True, related_name="posts")

    title = models.CharField(max_length=255,null=False)

    current_revision = models.OneToOneField('MainPostRevision', verbose_name=_('current revision'),
            null=True, blank=True, related_name = "revision_post")
    # type of the posts: questions; forum/discussion; blog; 
    QUESTION, DISCUSSION, BLOG = range(3)
    TYPE_CHOICE = [(QUESTION, "question"), (DISCUSSION, "discussion"), (BLOG, "blog")]
    type = models.IntegerField(choices=TYPE_CHOICE)
    # views for the post
    view_count = models.IntegerField(default=0)

    reply_count = models.IntegerField(default=0)

    bookmark_count = models.IntegerField(default=0)

    mainpost_votes = GenericRelation("utils.Vote")

    post_views = GenericRelation("utils.View")
    
    post_bookmark = GenericRelation("utils.Bookmark")

    accepted_answer = models.ForeignKey("ReplyPost", blank=True, null=True, related_name="accepted_root")
    main_post_comments = GenericRelation("utils.Comment")
    
    # marked duplicated post. 
    #duplicated_post = models.ForeignKey("self", blank=True, null=True)

    def __unicode__(self):
        return self.title

    @staticmethod
    def update_post_views(post, request, hours=24):
        "Views are updated per user session"

        # Extract the IP number from the request.
        ip1 = request.META.get('REMOTE_ADDR', '')
        ip2 = request.META.get('HTTP_X_FORWARDED_FOR', '').split(",")[0].strip()
        # 'localhost' is not a valid ip address.
        ip1 = '' if ip1.lower() == 'localhost' else ip1
        ip2 = '' if ip2.lower() == 'localhost' else ip2
        ip = ip2 or ip1 or '0.0.0.0'

        now = timezone.now()
        since = now - timezone.timedelta(hours=hours)

        obj_type = ContentType.objects.get_for_model(post)
        obj_id =post.id

        # One view per time interval from each IP address.
        if not post.post_views.filter(ip=ip, date__gt=since):
            new_view = View(ip=ip, content_object=post, date=now)
            new_view.save()
            MainPost.objects.filter(id=post.id).update(view_count=F('view_count') + 1)
        return post


    @staticmethod
    def reset_reply_count(sender, instance, **kwargs):
        post = instance.mainpost
        print post, post.replies.count()
        post.reply_count = post.replies.count()
        post.save()


    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs = {'pk': self.pk})

    def get_vote_count(self):
        return self.mainpost_votes.filter(choice=1).count() - self.mainpost_votes.filter(choice=-1).count()

    def get_reply_count(self):
        return self.replies.count()

    def get_comments(self):
        return self.main_post_comments.all()

class ReplyPost(AbstractPost):
    mainpost = models.ForeignKey(MainPost, related_name = "replies", null=False)
    current_revision = models.OneToOneField('ReplyPostRevision', blank=True, null=True, verbose_name=_('current revision'), 
        related_name="revision_post")
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


post_save.connect(MainPost.reset_reply_count, sender=ReplyPost)
post_delete.connect(MainPost.reset_reply_count, sender=ReplyPost)
