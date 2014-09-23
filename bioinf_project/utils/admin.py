from django.contrib import admin

from .models import Comment, Vote, View, Rate
# Register your models here.
admin.site.register((Comment,Vote, View, Rate))

