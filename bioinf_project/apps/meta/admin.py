from django.contrib import admin

from .models import Report, ReportRevision
# Register your models here.
admin.site.register((Report, ReportRevision))
