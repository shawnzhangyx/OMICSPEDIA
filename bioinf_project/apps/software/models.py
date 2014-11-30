from django.db import models
from django.forms import ModelForm
from django.contrib.contenttypes.generic import GenericRelation 
from django.core.urlresolvers import reverse

from wiki.models import Page 
from django.utils import timezone

# Create your models here.

# the information can be edited by anyone at first; 
# after it's been established, it will be protected, only authorized user 
# and moderators can edit the information. 
class Tool(models.Model):
    # other than the tool specific information, the other parts are the same as the wiki page. 
    page = models.OneToOneField("wiki.Page", related_name="software")
    # tool information
    name = models.CharField(max_length=255, blank=True, unique=True)
    image = models.ImageField(upload_to='software',null=True,blank=True)
    url = models.URLField(max_length=255,blank=True)
    language = models.CharField(max_length=255,blank=True)
    OS = models.CharField(max_length=255,blank=True)
    # license
    citation = models.CharField(max_length=255, blank=True)
    availability = models.CharField(max_length=255, blank=True)
    # author information
    author_name = models.CharField(max_length=255,blank=True)
    author_affiliation = models.CharField(max_length=255, blank=True)
    ## how the author prefer to be contacted wtih the tool problems.
    author_contacts = models.CharField(max_length=255, blank=True)
    #### we can add the author to the model if the author is using this website. 
    # author = models.ForeignKey('users.User')
    # release information
    first_release_date = models.DateField(null=True)
    latest_release_date = models.DateField(null=True)
    # feedbacks
    tool_votes = GenericRelation("utils.Vote")
    tool_comment = GenericRelation("utils.Comment")
    
    # status
    PUBLIC, PROTECTED, FREEZED = range(3)
    STATUS_CHOICE = [(PUBLIC,'open to public'), (PROTECTED,'protected'), (FREEZED,'freezed')]
    #status = models.IntergerField(choices=STATUS_CHOICE,default=0)

    def get_absolute_url(self):
        return reverse('software:software-detail', kwargs={'name':self.name})

    def get_vote_count(self):
        return self.tool_votes.filter(choice=1).count() - self.tool_votes.filter(choice=-1).count()
