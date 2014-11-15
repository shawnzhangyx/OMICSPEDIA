from django.db import models
from utils.models import AbstractBaseRevision
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from utils.models import View
from django.db.models import F
from django.conf import settings

# Create your models here.

class Flag(models.Model):
    # who created the flag
    flagger = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="flags")
    # link to the object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # why is it flagged.
    content = models.TextField(verbose_name = _("content"), null=False, blank=False)
    

class Report(models.Model):
    title = models.CharField(_("title"), max_length=255, unique=True)
    current_revision = models.OneToOneField('ReportRevision', blank=True, null=True, verbose_name=_('current revision'),
                                            related_name = "revision_page")
    report_votes = GenericRelation("utils.Vote")
    report_comments = GenericRelation("util.Comment")
    report_views = GenericRelation("utils.View")
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,blank=False,null=False)
    created = models.DateTimeField()
    last_modified = models.DateTimeField()

    #---- functions ----#
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.last_modified = timezone.now()
        return super(Report, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_vote_count(self):
        return self.report_votes.filter(choice=1).count() - self.report_votes.filter(choice=-1).count()

    def get_comments(self):
        return self.report_comments.all()
    def get_comment_count(self):
        return 0#self.report_comments.all.count()

    def get_absolute_url(self):
        return reverse('meta:meta-index')

    @staticmethod
    def update_report_views(report, request, minutes=60):
        "Views are updated per user session"

        # Extract the IP number from the request.
        ip1 = request.META.get('REMOTE_ADDR', '')
        ip2 = request.META.get('HTTP_X_FORWARDED_FOR', '').split(",")[0].strip()
        # 'localhost' is not a valid ip address.
        ip1 = '' if ip1.lower() == 'localhost' else ip1
        ip2 = '' if ip2.lower() == 'localhost' else ip2
        ip = ip1 or ip2 or '0.0.0.0'

        now = timezone.now()
        since = now - timezone.timedelta(minutes=minutes)

        obj_type = ContentType.objects.get_for_model(report)
        obj_id =report.id

        # One view per time interval from each IP address.
        if not report.report_views.filter(ip=ip, date__gt=since):
            new_view = View(ip=ip, content_object=report, date=now)
            new_view.save()
            Report.objects.filter(id=report.id).update(view_count=F('view_count') + 1)
        return report

class ReportRevision(AbstractBaseRevision):
    report = models.ForeignKey("Report", on_delete = models.CASCADE, verbose_name=_("report"))

    def __unicode__(self):
        return self.report.title+"_revision_"+str(self.revision_number)


    def save(self, *args, **kwargs):
        if not self.revision_number:
            try:
                previous_revision = self.report.reportrevision_set.latest()
                self.revision_number = previous_revision.revision_number + 1
            except ReportRevision.DoesNotExist:
                self.revision_number = 1
        super(ReportRevision, self).save(*args, **kwargs)

