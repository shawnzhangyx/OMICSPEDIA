from django.db import models
from django.db.models import F
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import m2m_changed, post_save, pre_delete

from django.conf import settings

from posts.models import MainPost, ReplyPost

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
    icon = models.ImageField(upload_to='tags',null=True,blank=True)
    wiki_page = models.OneToOneField("wiki.Page", related_name='wiki_tag')
    # record the times this tag is used
    count = models.IntegerField(default=0)
    # record the bookmark count of this tag.
    #bookmark_count = models.IntegerField(default=0)

    # provide the tag structures
    # can chain Tags that have tree structures.
    parent = models.ForeignKey('self', related_name = "children",null=True, blank=True)
    node_position = models.IntegerField(default=0)

    # the types of the tag
    PROPOSED, PROTECTED = range(2) 
    STATUS_CHOICE = [(PROPOSED, "proposed"), (PROTECTED, "protected")]
    status = models.IntegerField(choices=STATUS_CHOICE, default=PROPOSED)
    REGULAR, WORKFLOW, SOFTWARE = range(3)
    CATEGORY_CHOICE = [(REGULAR,"regular"), (WORKFLOW,"workflow"), (SOFTWARE,"software")]
    categories = models.IntegerField(choices=CATEGORY_CHOICE, default=REGULAR)

    def questions(self):
        return self.posts.filter(type=0)
        
    def discussions(self):
        return self.posts.filter(type=1)
        
    def blogs(self):
        return self.posts.filter(type=2)
    
    
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

    def name_underlined(self):
        return self.name.replace(' ','_')

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

class Meta:
        get_latest_by= 'node_position'
    #---- methods ----#
   # def __init__(self, *args, **kwargs):
   #     pass

# this tabel is used to save the number of answers users made on each tag
class UserTag(models.Model):
    tag = models.ForeignKey('Tag', related_name="usertags")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="usertags")
    answer_count = models.IntegerField(default=0)
    answers = models.ManyToManyField('posts.ReplyPost', null=True, blank=True)
    
    def __unicode__(self):
        return u"%s,%s,%s" %(self.tag.name, self.user.user_profile.name, self.answer_count)
    
    
    
    @staticmethod
    def answer_update_due_to_m2m_change(sender, instance, action, pk_set, *args, **kwargs):
        "Applies answer updates upon post changes"
        if action == 'pre_clear':
            affected_tags = instance.tags.all()
        elif action == 'post_add' or action == 'post_remove':
            affected_tags = Tag.objects.filter(pk__in=pk_set)
        else:
            return
            
        for answer in instance.replies.all(): 
            for tag in affected_tags: 
                usertag = UserTag.objects.get_or_create(tag=tag, user=answer.author)[0]
                if action == 'post_add':
                    usertag.answers.add(answer)
                    usertag.answer_count += 1
                elif action == 'post_remove' or action == "pre_clear":
                    usertag.answers.remove(answer)
                    usertag.answer_count -= 1
                usertag.save()
                
    @staticmethod            
    def answer_update_due_to_answer_add(sender, instance, **kwargs):
        #instance.save()
        for tag in instance.mainpost.tags.all(): 
            usertag = UserTag.objects.get_or_create(tag=tag, user=instance.author)[0]
            if instance not in usertag.answers.all():
                usertag.answers.add(instance)
                usertag.answer_count += 1
                usertag.save()
            
    @staticmethod   
    def answer_update_due_to_answer_delete(sender, instance, **kwargs):
        for tag in instance.mainpost.tags.all(): 
            usertag = UserTag.objects.get_or_create(tag=tag, user=instance.author)[0]
            usertag.answers.remove(instance)
            usertag.answer_count -= 1
            usertag.save()
            
    class Meta: 
        unique_together = ('tag', 'user')

# data signals
m2m_changed.connect(Tag.update_tag_counts, sender=MainPost.tags.through)
m2m_changed.connect(UserTag.answer_update_due_to_m2m_change, sender=MainPost.tags.through)
post_save.connect(UserTag.answer_update_due_to_answer_add, sender=ReplyPost)
pre_delete.connect(UserTag.answer_update_due_to_answer_delete, sender=ReplyPost)

