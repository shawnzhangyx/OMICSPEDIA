from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation 
from django.utils import timezone
#from django.contrib.auth.models import User
import markdown
from utils import diff_match_patch
from utils.models import AbstractBaseRevision
import re
from django.conf import settings
# Create your models here.

# Ideally, every tag should have a wiki,
# but not every wiki should have a tag.
# so it may be oneToOne relationship from Tag to Wiki Page.
class Page(models.Model):

    title = models.CharField(_("title"), max_length=255, unique=True)
    tags = models.ManyToManyField("tags.Tag",blank=True, related_name="pages")
    #wiki_votes = GenericRelation("utils.Vote")
    #wiki_rates = GenericRelation("utils.Rate")
    wiki_bookmark = GenericRelation("utils.Bookmark")

    # count of things
    bookmark_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    current_revision = models.OneToOneField('PageRevision', blank=True, null=True, verbose_name=_('current revision'),
                                            related_name = "revision_page")
    # redirect url
    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title.replace(" ", "_")

    def get_lead_section(self):
        #(\[TOC\])?\r\n#(.|\n)*$
        pattern = re.compile(u'^\s*?((.|\n)*?)\s*?(\n#(.|\n)*)?$')
        match = re.search(pattern, self.current_revision.content)
        lead_raw = match.group(1)
        toc = re.compile(u'\[TOC\]')
        lead = re.sub(toc,'', lead_raw)
        return markdown.markdown(lead,
        extensions=['extra',
                    'wikilinks(base_url=/wiki/, end_url=/)',],
        safe_mode='escape')

    def get_rate_average(self):
        rate_count = self.wiki_rates.count()
        rate_sum = 0
        for rate in self.wiki_rates.all():
                rate_sum += rate.rating
        if rate_count > 0:
            return float(rate_sum)/rate_count
        else:
            return rate_sum
    
    def get_absolute_url(self):
        return reverse('wiki:wiki-detail', kwargs = {'title': self.get_title()})

class PageRevision(AbstractBaseRevision):

    page = models.ForeignKey(Page, on_delete = models.CASCADE, verbose_name=_("page"))
    total_chars = models.IntegerField(_('total_chars'))
    added_chars = models.IntegerField(_('added_chars'))
    deleted_chars = models.IntegerField(_('deleted_chars'))

    def __unicode__(self):
        return self.page.title+"_revision_"+str(self.revision_number)


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

class PageComment(models.Model):
    # the status of the comment
    OPEN, PENDING, CLOSED = range(3)
    STATUS_CHOICE = [(OPEN, "open"), (PENDING,"close pending"), (CLOSED,"closed")]
    status = models.IntegerField(choices=STATUS_CHOICE, default=OPEN)
    # the type of the comment; this can be substitute as a subtype of issues. 
    ISSUE, REQUEST, DISCUSS = range(3)
    COMMENT_TYPE_CHOICE = [(ISSUE, "issue"), (REQUEST, "request"), (DISCUSS, "discuss")]
    comment_type = models.IntegerField(choices=COMMENT_TYPE_CHOICE, default="discuss")
    # This is only required when the user report issue
    GRAMMER, WIKILINK, EXPAND, CHECK_REFERENCE, ADD_REFERENCE, IMAGE, LEAD, NEW_INFO = range(8)
    ISSUE_CHOICE = [(GRAMMER,'fix spelling and gramma'),
            (WIKILINK, 'fix wikilink'), (EXPAND, 'expand short article'),
            (CHECK_REFERENCE, 'check reference'), (ADD_REFERENCE, 'add reference'),
            (IMAGE, 'add image'), (LEAD, 'Improve lead section'),
            (NEW_INFO,'add new information')]
    issue = models.IntegerField(choices=ISSUE_CHOICE, null=True)
    # the details of the comment
    detail = models.TextField(verbose_name = _("detail"), blank=True)
    page = models.ForeignKey("Page", related_name="comments")
    init_revision = models.ForeignKey("PageRevision", related_name="comment_init",blank=True,null=True)
    # instead of final version, show revised version. 
    final_revision = models.ForeignKey("PageRevision", related_name="comment_closed",blank=True,null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("author"))
    created = models.DateTimeField(_("created date"))
    modified = models.DateTimeField(_("modifed date"),auto_now=True)
    
    def __unicode__(self):
        return self.get_comment_type_display() + ': ' + self.get_issue_display()
        
    def get_absolute_url(self):
        return reverse('wiki:wiki-comment', kwargs = {'title': self.page.get_title()})
        
    def get_status_class(self):
    # OPEN, PENDING, CLOSED = range(4)
        dict = {self.OPEN:"btn-danger", 
        self.PENDING:"btn-success", self.CLOSED:"btn-default"}
        return dict[self.status]
        
    def get_issue_warnings_message(self):
    # GRAMMER, WIKILINK, EXPAND, CHECK_REFERENCE, ADD_REFERENCE, IMAGE, LEAD, NEW_INFO = range(8)        
        dict = {self.GRAMMER: 'There is grammer error in this page',
                self.WIKILINK: 'Some wikilink may be not functional',
                self.EXPAND: 'This page is too short, please expand it',
                self.CHECK_REFERENCE: 'References may be inaccurate',
                self.ADD_REFERENCE: 'Rerefences are largely missing',
                self.IMAGE:'add some image',
                self.LEAD:'please improve the lead section of this page',
                self.NEW_INFO:'please provide some new information on this page'}
        return dict[self.issue]
# --------- #
# a page can have several sections, instead of just one giant
# piece of content, this will make editing more convenient.
# setting it up now, but will not use it in demonstration.

