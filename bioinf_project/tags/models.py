from django.db import models

# Create your models here.
class Tag(models.Model):
    def __unicode__(self):
        return self.name
        
    #---- fields ----#
    name = models.CharField(max_length=255)
    # record the times this tag is used
    count = models.IntegerField(default=1)
    
    # provide the tag structures
    # can chain Tags that have tree structures. 
    #? parent = models.OnetoOneField('self',null=True,blank=T)
    parent = models.ForeignKey('self', related_name = "children",null=True, blank=True)
    sibling_before = models.ForeignKey('self', related_name = "after",null=True, blank=True)
    sibling_after = models.ForeignKey('self', related_name = "before",null=True, blank=True)
    
    # the types of the tag
    PROPOSED, APPROVED, WORKFLOW, SOFTWARE = range(4)
    CATEGORY_CHOICE = [(PROPOSED, "proposed"), (APPROVED,"approved"), (WORKFLOW,"workflow"), (SOFTWARE,"software")]
    categories = models.IntegerField(choices=CATEGORY_CHOICE, default=PROPOSED)
    #---- methods ----#
    # check if the tag is the root. 
    def is_root():
        pass
    # check if the tag is duplicated. 
    def is_same():
        pass
    # ---- #

    
