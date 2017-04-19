from django.contrib import admin

from .models import Comment, Vote, View, Rate, Bookmark, ImageAttachment, Search
# Register your models here.
admin.site.register((Comment,Vote, View, Rate, Bookmark, ImageAttachment, Search))

