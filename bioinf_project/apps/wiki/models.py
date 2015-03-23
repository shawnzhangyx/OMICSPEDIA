from django.db import models
from django.db.models import F
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation 
from django.utils import timezone
from django.db.models.signals import m2m_changed, post_save, pre_delete

import markdown
from utils import diff_match_patch
from utils.models import AbstractBaseRevision, View
import re
from django.conf import settings
# Create your models here.


class UniquePageManager(models.Manager):
    def get_queryset(self):
        return super(UniquePageManager, self).get_queryset().filter(redirect_to__isnull = True)

# Ideally, every tag should have a wiki,
# but not every wiki should have a tag.
# so it may be oneToOne relationship from Tag to Wiki Page.
class Page(models.Model):

    objects = models.Manager()
    uniques = UniquePageManager() 

    title = models.CharField(_("title"), max_length=255, unique=True)
    tags = models.ManyToManyField("tags.Tag",blank=True, related_name="pages")
    redirect_to = models.OneToOneField("Page", blank=True, null=True)
    #wiki_votes = GenericRelation("utils.Vote")
    #wiki_rates = GenericRelation("utils.Rate")
    wiki_views = GenericRelation("utils.View")
    view_count = models.IntegerField(default=0)
    wiki_bookmark = GenericRelation("utils.Bookmark")
    image_attachment = GenericRelation("utils.ImageAttachment")
    # count of things
    bookmark_count = models.IntegerField(default=0)
    # number of comment count, used for sorting. 
    open_comment_count = models.IntegerField(default=0)
    pending_comment_count = models.IntegerField(default=0)
    
    current_revision = models.OneToOneField('PageRevision', blank=True, null=True, verbose_name=_('current revision'),
                                            related_name = "revision_page")
                                            
    OPEN, PROTECTED = range(2)
    STATUS_CHOICE = [(OPEN, "open"), (PROTECTED,"protected")]
    status = models.IntegerField(choices=STATUS_CHOICE, default=OPEN)
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
    
    def get_open_comment(self):
        return self.comments.filter(status = 0)
        
    def get_pending_comment(self):
        return self.comments.filter(status = 1)
        
    def get_closed_comment(self):
        return self.comments.filter(status = 2)
        
        
    @staticmethod
    def update_wiki_views(wiki, request, hours=24):
        "Views are updated per user session"

        # Extract the IP number from the request.
        ip1 = request.META.get('REMOTE_ADDR', '')
        ip2 = request.META.get('HTTP_X_FORWARDED_FOR', '').split(",")[0].strip()
        # 'localhost' is not a valid ip address.
        ip1 = '' if ip1.lower() == 'localhost' else ip1
        ip2 = '' if ip2.lower() == 'localhost' else ip2
        ip = ip2 or ip1 or '0.0.0.0'

        now = timezone.now()
        since = now - timezone.timedelta(hours=hours)

        obj_type = ContentType.objects.get_for_model(wiki)
        obj_id =wiki.id
        # One view per time interval from each IP address.
        if not wiki.wiki_views.filter(ip=ip, date__gt=since):
            new_view = View(ip=ip, content_object=wiki, date=now)
            new_view.save()
            Page.objects.filter(id=wiki.id).update(view_count=F('view_count') + 1)
        return wiki
    
    @staticmethod
    def reset_comment_count():
        for wiki in Page.objects.all():
            wiki.open_comment_count = wiki.get_open_comment().count()
            wiki.pending_comment_count = wiki.get_pending_comment().count()
            wiki.save()
            
    @staticmethod        
    def update_comment_count(sender, instance, **kwargs):
        page = instance.page
        page.open_comment_count = page.get_open_comment().count()
        page.pending_comment_count = page.get_pending_comment().count()
        page.save()
        
    def get_absolute_url(self):
        return reverse('wiki:wiki-detail', kwargs = {'title': self.get_title()})


class PageRevision(AbstractBaseRevision):

    page = models.ForeignKey(Page, on_delete = models.CASCADE, verbose_name=_("page"), related_name="all_revisions")
    total_chars = models.IntegerField(_('total_chars'))
    added_chars = models.IntegerField(_('added_chars'))
    deleted_chars = models.IntegerField(_('deleted_chars'))

    def __unicode__(self):
        return self.page.title+"_revision_"+str(self.revision_number)


    def save(self, *args, **kwargs):
        if not self.revision_number:
            try:
                previous_revision = self.page.all_revisions.latest()
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
    OTHER, GRAMMER, LINK, EXPAND, CHECK_REFERENCE, ADD_REFERENCE, IMAGE, LEAD, NEW_INFO = range(9)
    ISSUE_CHOICE = [(OTHER, 'other'), (GRAMMER,'fix spelling and gramma'),
            (LINK, 'fix link'), (EXPAND, 'expand short article'),
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
        
    class Meta: 
        get_latest_by= 'created'
# --------- #

post_save.connect(Page.update_comment_count, sender=PageComment)


class UserPage(models.Model):
    page = models.ForeignKey('Page', related_name="userpage")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name ="userpage")
    revisions = models.ManyToManyField('PageRevision', null=True, blank=True)
    edits = models.IntegerField(default=0)
    added = models.IntegerField(default=0)
    deleted = models.IntegerField(default=0)
    
    @staticmethod 
    def update_due_to_new_revision(sender, instance, **kwargs):
        userpage = UserPage.objects.get_or_create(page=instance.page, user=instance.author)[0]
        userpage.edits += 1
        userpage.added += instance.added_chars
        userpage.deleted += instance.deleted_chars
        userpage.revisions.add(instance)
        userpage.save()
        
    @staticmethod 
    def update_due_to_deleted_revision(sender, instance, **kwargs):
        userpage = UserPage.objects.get_or_create(page=instance.page, user=instance.author)[0]
        userpage.edits -= 1
        userpage.added -= instance.added_chars
        userpage.deleted -= instance.deleted_chars
        userpage.revisions.remove(instance)
        userpage.save()
        
    def reset_userpage(self):
        page = self.page
        revisions = page.all_revisions.filter(author=self.user)
        self.edits = revisions.count()
        self.added = 0
        self.deleted = 0
        if revisions.count() >= 1:
            for revision in revisions:
                self.added += revision.added_chars
                self.deleted += revision.deleted_chars
                self.revisions.add(revision)
        self.save()
    
    @staticmethod
    def collect_userpage():
        userpage_list = []
        for page in Page.objects.all():
            for revision in page.all_revisions.all():
                userpage = UserPage.objects.get_or_create(page=page, user=revision.author)[0]
                if userpage not in userpage_list:
                    userpage_list.append(userpage)
        
        for userpage in userpage_list:
            userpage.reset_userpage()
        
        
    class Meta: 
        unique_together = ('page', 'user')
        
        
post_save.connect(UserPage.update_due_to_new_revision, sender=PageRevision)
pre_delete.connect(UserPage.update_due_to_deleted_revision, sender=PageRevision)
