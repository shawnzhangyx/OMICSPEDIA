from django.db import models
from django.db.models import F
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import m2m_changed

from posts.models import MainPost

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

class Tag(models.Model):

    #custom manager
    objects = TagManager()

    #---- fields ----#
    name = models.CharField(max_length=255, unique=True)
    wiki_page = models.OneToOneField("wiki.Page",blank=True, null=True)
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

    @staticmethod
    def update_tag_counts(sender, instance, action, pk_set, *args, **kwargs):
        "Applies tag count updates upon post changes"

        if action == 'post_add':
            Tag.objects.filter(pk__in=pk_set).update(count=F('count') + 1)

        if action == 'post_remove':
            Tag.objects.filter(pk__in=pk_set).update(count=F('count') - 1)

        if action == 'pre_clear':
            instance.tags.all().update(count=F('count') - 1)

    @staticmethod
    def reset_tag_counts():
        for tag in Tag.objects.all():
            print tag, tag.posts.count()
            tag.count = tag.posts.count()
            tag.save()

    class Meta:
        get_latest_by= 'node_position'
    #---- methods ----#
   # def __init__(self, *args, **kwargs):
   #     pass

    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('tags:tag-detail', kwargs = {'name': self.name})
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


# data signals
m2m_changed.connect(Tag.update_tag_counts, sender=MainPost.tags.through)
