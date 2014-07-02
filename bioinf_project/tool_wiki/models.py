from django.db import models

from tags.models import Tag
from wiki.models import Page 

# Create your models here.
class Tool(Page):
    author = models.CharField(max_length=100)
    author_email = models.EmailField(blank=True)
    version = models.CharField(max_length=100)
    # latest release date might not be accurate, 
    # depending on the last time someone checked it. 
    latest_release_date = models.DateField(blank=True)
    # whether it's maintained is more useful information to know
    maintained = models.NullBooleanField()
    creation_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    
# other than the tool specific information, the other parts are the same as the wiki page. 
