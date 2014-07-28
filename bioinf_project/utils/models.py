from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation, GenericForeignKey
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
    content = models.TextField(max_length=600, null=False)
    last_modified = models.DateTimeField()
    ## enable generic foreignkey relationship with other classes, such as Page, MainPost, ReplyPost. 
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.content[:25]
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.last_modified = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    class Meta: 
        get_latest_by = "-last_modified"


class Vote(models.Model):
    # votes for a post, wiki, tool, or tag, user. Or anything else you can think. 
    UP, NEUTRAL, DOWN = range(3)
    CHOICES = [(UP, "Up-vote"), (NEUTRAL, "Neutral"), (DOWN, "Down-vote")]
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    choice = models.IntegerField(choices=CHOICES, default=1)
    date = models.DateField(auto_now=True)
    
    def __unicode__(self):
        return u"%s, %s, %s" %( self.get_choice_display(), self.user.username, self.content_object.id) 

    class Meta: 
        unique_together = (("user", "content_type"),)

## class Views(
