from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, UserProfile, Notification
# Register your models here.
admin.site.register((User, UserProfile, Notification,))
