from django.contrib import admin
from .models import Page, PageRevision, PageComment, UserPage

# Register your models here.
admin.site.register((Page, PageRevision, PageComment, UserPage))

