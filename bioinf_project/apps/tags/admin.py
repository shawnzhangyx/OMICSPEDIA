from django.contrib import admin
from .models import Tag, UserTag

# Register your models here.
admin.site.register((Tag, UserTag))

