from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation, GenericForeignKey
from django.utils import timezone

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

