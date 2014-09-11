from django.contrib import admin
from .models import Page, PageRevision, PageComment

# Register your models here.
admin.site.register((Page, PageRevision, PageComment))

