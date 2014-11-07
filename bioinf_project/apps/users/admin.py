from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, UserProfile
# Register your models here.
admin.site.register((User, UserProfile,))
