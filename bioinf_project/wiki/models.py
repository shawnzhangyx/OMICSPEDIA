from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation 
from django.utils import timezone
from django.contrib.auth.models import User
import markdown
from utils import diff_match_patch

# Create your models here.

# Ideally, every tag should have a wiki, 
# but not every wiki should have a tag. 
# so it may be oneToOne relationship from Tag to Wiki Page. 
class Page(models.Model):

    title = models.CharField(_("title"), max_length=255, unique=True)
    tags = models.ManyToManyField("tags.Tag",blank=True) 
    comments = GenericRelation("utils.Comment")
    wiki_votes = GenericRelation("utils.Vote")
    current_revision = models.OneToOneField('PageRevision', blank=True, null=True, verbose_name=_('current revision'),
                                            related_name = "revision_page")
    # created_date = models.DateTimeField(_('created date'))                                        
    # author_list and their contributions. 
    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title.replace(" ", "_")

    def get_marked_up_content(self):
        return markdown.markdown(self.current_revision.content, 
                extensions=['extra','wikilinks(base_url=/wiki/, end_url=/)','toc'])

    def get_vote_count(self):        
        return self.wiki_votes.filter(choice=1).count() - self.wiki_votes.filter(choice=-1).count()

    def get_absolute_url(self):
        return reverse('wiki:wiki-detail', kwargs = {'title': self.get_title()})

class PageRevision(models.Model):
    revision_number = models.IntegerField(_('revision number'), editable=False)
    revision_summary = models.TextField(_('revision summary'), blank=True)
    # previous_revision = models.ForeignKey('self', verbose_name=_("previous revision"), blank=True, null=True)
    # editor = models.ForeignKey(User, blank=True, null = True)
    page = models.ForeignKey(Page, on_delete = models.CASCADE, verbose_name=_("page"))
    content = models.TextField(blank=True, verbose_name = _("page content"))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_("modified date"))
    author = models.ForeignKey(User)
    total_chars = models.IntegerField(_('total_chars'))
    added_chars = models.IntegerField(_('added_chars'))
    deleted_chars = models.IntegerField(_('deleted_chars'))

    def __unicode__(self):
        return self.page.title+"_revision_"+str(self.revision_number)

    def get_marked_up_content(self):
        return markdown.markdown(self.content,
               extensions=['extra','wikilinks(base_url=/wiki/, end_url=/)','toc'])

    def save(self, *args, **kwargs):
        if not self.revision_number:
            try:
                previous_revision = self.page.pagerevision_set.latest()
                self.revision_number = previous_revision.revision_number + 1
            except PageRevision.DoesNotExist:
                self.revision_number = 1
        self.cal_add_delete_chars()
        super(PageRevision, self).save(*args, **kwargs)

    def get_pre_revision(self):
        try:
            return PageRevision.objects.get(revision_number = self.revision_number - 1, page = self.page)
        except PageRevision.DoesNotExist:
            return

    def cal_add_delete_chars(self):
        if self.revision_number == 1:
            text1 = ""
        else:
            text1 = self.get_pre_revision().content
        text2 = self.content 
        func = diff_match_patch.diff_match_patch()
        diff = func.diff_main(text1, text2)
        added = 0
        deleted = 0
        for (sign, frag) in diff:
            if sign == 1:
                added += len(frag)
            elif sign == -1:
                deleted += len(frag)
        self.added_chars = added
        self.deleted_chars = deleted
        self.total_chars = len(text2)
    class Meta:
        get_latest_by= 'revision_number'



# --------- #
# a page can have several sections, instead of just one giant 
# piece of content, this will make editing more convenient. 
# setting it up now, but will not use it in demonstration. 

