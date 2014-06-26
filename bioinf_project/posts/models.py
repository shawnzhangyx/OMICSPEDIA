#django core modules
from django.db import models

#local apps
from tags.models import Tag

# Create your models here.

# --------------- #
# Can have an abstract Post class and two differen children: MainPost and Replies #
# For now, we just follow the Biostar standard. #
class Post(models.Model):
    def __unicode__(self):
        return self.title
        
    title = models.CharField(max_length=255,null=False)
    content = models.TextField(default='Enter here')
    root = models.ForeignKey('self', related_name = "replies", null=True, blank=True)
    parent = models.ForeignKey('self', related_name = "children",null=True, blank=True)
    vote_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag,blank=True,)
    creation_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    
    ### potential useful fields: 
    # author
    