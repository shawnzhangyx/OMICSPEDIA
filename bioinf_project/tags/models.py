from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from wiki.models import Page
# Create your models here.
class TagManager(models.Manager):

    def get_tag_search_list(self, max_results=0, contains=''):
        tag_list = []
        if contains:
            tag_list = self.filter(name__icontains=contains)
        else:
            tag_list = self.all()
        if max_results > 0: 
            if len(tag_list) > max_results:
                tag_list = tag_list[:max_results]
#        for cat in cat_list: 
#            cat.url = encode_url(tag.name)
        return tag_list

class Tag(Page):
    
    #custom manager
    objects = TagManager()
    
    #---- fields ----#
    name = models.CharField(max_length=255, unique=True)
    parent_page = models.OneToOneField("wiki.Page",parent_link=True)
    # record the times this tag is used
    count = models.IntegerField(default=0)
    # provide the tag structures
    # can chain Tags that have tree structures. 
    parent = models.ForeignKey('self', related_name = "children",null=True, blank=True)
    node_position = models.IntegerField(default=0)
    
    # the types of the tag
    PROPOSED, APPROVED, WORKFLOW, SOFTWARE = range(4)
    CATEGORY_CHOICE = [(PROPOSED, "proposed"), (APPROVED,"approved"), (WORKFLOW,"workflow"), (SOFTWARE,"software")]
    categories = models.IntegerField(choices=CATEGORY_CHOICE, default=PROPOSED)
    
    class Meta: 
        get_latest_by= 'node_position'
    #---- methods ----#
   # def __init__(self, *args, **kwargs):
   #     pass
   
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('tags:tag-detail', kwargs = {'pk': self.pk})
    # check if the tag is the root. 
    def is_root():
        pass
    # check if the tag is duplicated. 
    def is_same():
        pass
    # ---- #
    # adjust the node position among children under the same parent.
    def adjust_pos():
        pass
    
