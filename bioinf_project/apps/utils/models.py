from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation, GenericForeignKey
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import markdown
# Create your models here.
# Base revision model.
class AbstractBaseRevision(models.Model):
    # ultimately, we don't need the revision number at all,
    # we can sort the revisions by the date.
    revision_number = models.IntegerField(verbose_name=_('revision number'))
    # revision type (short summary)? correct grammar; fix link; add content; e.t.c.
    revision_summary = models.CharField(max_length=20, blank=True, verbose_name=_('revision summary'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_("modified date"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("author"))
    content = models.TextField(blank=True, verbose_name=_("content"))

    def get_marked_up_content(self):
        return markdown.markdown(self.content,
        extensions=['extra',
                    'wikilinks(base_url=/wiki/, end_url=/)',
                    'toc'],
        safe_mode='escape')

    class Meta:
        abstract=True
        get_latest_by= 'modified_date'

# Base content model that uses the revision.
class AbstractBasePage(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name=_("title"))
    tags = models.ManyToManyField("tags.Tag",blank=True, verbose_name=_("tags"))
    class Meta:
        abstract=True


# should refactor this to be base comment.
class Comment(models.Model):
    content = models.TextField(max_length=600, null=False, verbose_name=_("content"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("author"))
    comment_votes = GenericRelation("Vote")
    created = models.DateTimeField(verbose_name=_("created time"))
    last_modified = models.DateTimeField()
    ## enable generic foreign key relationship with other classes, such as Page, MainPost, ReplyPost. 
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.content[:25]
        
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.created:
            self.created = timezone.now()
        self.last_modified = timezone.now()
        return super(Comment, self).save(*args, **kwargs)
        
    def get_vote_count(self):
        return self.comment_votes.filter(choice=1).count() - self.comment_votes.filter(choice=-1).count()
    class Meta:
        get_latest_by = "-last_modified"


class Vote(models.Model):
    # votes for a post, wiki, tool, or tag, user. Or anything else you can think.
    UP, DOWN = [1,-1]
    CHOICES = [(UP, "Up-vote"), (DOWN, "Down-vote")]
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="votes", verbose_name=_("voter"))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    choice = models.IntegerField(choices=CHOICES)
    date = models.DateField(auto_now=True)

    def __unicode__(self):
        return u"%s, %s, %s" %( self.get_choice_display(), self.voter.email, self.content_type.id)

    class Meta:
       unique_together = ("voter", "content_type","object_id")

class View(models.Model):
    # viewer IP
    ip = models.GenericIPAddressField(default="", null=True, blank=True, verbose_name=_("IP"))
    # date
    date = models.DateTimeField(auto_now=True)
    # viewed object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Rate(models.Model):
    # rate for a post, wiki, tool, or tag, user. Or anything else you can think.
    rating = models.IntegerField(verbose_name=_('rating'))
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rates")
    date = models.DateField(auto_now=True)
    # Rated object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    class Meta:
       unique_together = ("rater", "content_type","object_id")


    def __unicode__(self):
        return u"%s, %s, %s" %( self.rating, self.rater.email, self.content_object.id)


class Bookmark(models.Model):
    # reader
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="bookmarks")
    # date
    date = models.DateTimeField(auto_now=True)
     # Bookmarked object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u"%s, %s" %( self.reader.email, self.content_object.id)  
        
    class Meta: 
        unique_together = ("reader", "content_type", "object_id")        

        
    
    