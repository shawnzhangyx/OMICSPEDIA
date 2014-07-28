from django.db import models
from django.forms import ModelForm

from tags.models import Tag
from wiki.models import Page 
from django.utils import timezone

# Create your models here.
class Tool(Page):
    author = models.CharField(max_length=100)
    author_email = models.EmailField(blank=True)
    version = models.CharField(max_length=100,blank=True)
    # latest release date might not be accurate, 
    # depending on the last time someone checked it. 
    first_release_date = models.DateField(blank=True)
    latest_release_date = models.DateField(blank=True)
    # whether it's maintained is more useful information to know
    maintained = models.NullBooleanField(blank=True)
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id: 
            self.created = timezone.now()
        self.last_modified = timezone.now()
        return super(Tool, self).save(*args, **kwargs)
 
# other than the tool specific information, the other parts are the same as the wiki page. 


class ToolForm(ModelForm):
    class Meta: 
        model = Tool 
        fields = ['title', 'content','tags']

