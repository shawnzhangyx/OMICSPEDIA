from django.contrib import admin

from .models import Comment, Vote
# Register your models here.
admin.site.register((Comment,Vote))

