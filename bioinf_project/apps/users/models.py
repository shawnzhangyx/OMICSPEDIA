from django.db import models
from django.contrib.auth.models import User
# Create your models here.


###  atrributes of a user model:
# username, first_name, last_name, e-mail, password
# groups, user_permissions, is_staff, is_active, is_superuser
# last_login, date_joined
### methods:
# get_username, is_anonyous, is_authenticated, get_full_name, get_short_name
# set_password, check_password, has_perm, has_perms, email_user

class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name="user_profile")
    website = models.URLField(blank=True)
    biography = models.TextField(blank=True)
#    portrait = models.ImageField(null=True)
    reputation = models.IntegerField(default=1)
    #email = models.EmailField(blank=True)
    following = models.ManyToManyField('self',blank=True, related_name = "follower")

    def __unicode__(self):
        return self.user.username
