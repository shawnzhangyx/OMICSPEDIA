from django.db import models
from django.forms import ModelForm
from django.core.urlresolvers import reverse

from tags.models import Tag

# Create your models here.

# Ideally, every tag should have a wiki, 
# but not every wiki should have a tag. 
# so it may be oneToOne relationship from Tag to Wiki Page. 
class Page(models.Model):
    def __unicode__(self):
        return self.title
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag) 
    content = models.TextField(blank=True)
    # author_list and their contributions. 
    def get_absolute_url(self):
        return reverse('wiki:wiki-detail', kwargs = {'pk': self.pk})

class PageForm(ModelForm):
    class Meta: 
        model = Page
        fields = ['title', 'content','tags']
 
# --------- #
# a page can have several sections, instead of just one giant 
# piece of content, this will make editing more convenient. 
# setting it up now, but will not use it in demonstration. 
class Section(models.Model):
    def __unicode__(self):
        return self.section_title
        
    section_title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    
    
