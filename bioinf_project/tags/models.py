from django.db import models

# Create your models here.
class Tag(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=255)
    # record the times this tag is used
    count = models.IntegerField(default=1)
    # ---- #
    # can chain Tags that have tree structures. 
    #parent = models.OnetoOneField('self',null=True,blank=T)
    
