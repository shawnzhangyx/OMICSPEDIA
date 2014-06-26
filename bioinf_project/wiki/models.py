from django.db import models

from tags import Tag
# Create your models here.

# Ideally, every tag should have a wiki, 
# but not every wiki should have a tag. 
# so it may be oneToOne relationship from Tag to Wiki Page. 
class Page(models.Model):
    def __unicode__(self):
        return self.title
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    tag = models.ManyToManyField(Tag) 
    # author_list and their contributions. 
    
    
# --------- #
# a page can have several sections, instead of just one giant 
# piece of content, this will make editing more convenient. 
# setting it up now, but will not use it in demonstration. 
class Section(models.Model):
    def __unicode__(self):
        return self.section_title
        
    section_title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    
    