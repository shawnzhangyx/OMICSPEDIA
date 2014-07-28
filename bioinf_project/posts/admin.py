from django.contrib import admin
from .models import MainPost, MainPostRevision, ReplyPost, ReplyPostRevision
# Register your models here.
admin.site.register((MainPost, MainPostRevision,ReplyPost, ReplyPostRevision))
