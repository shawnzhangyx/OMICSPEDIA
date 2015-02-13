from django import template
from django.http import HttpResponse
from tags.models import Tag
from django.core.urlresolvers import reverse
register = template.Library()


#list the tags according to their hierarchical structure.

@register.inclusion_tag("users/templatetags/display_user_md.html")
def display_user_md(user, field):
    return {'user_profile': user, 'field': field}
    
    
@register.inclusion_tag("users/templatetags/display_user_xs.html")
def display_user_xs(user):
    return {'user': user}
    
@register.simple_tag
def display_verification_message():
    return "<span class='alert alert-warning'>only verified user has this privilege. <a href='"+reverse("users:email-verification-form", kwargs={'sent':''})+ "'>Verify your email</a> now?</span>"