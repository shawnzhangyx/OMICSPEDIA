from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Permission, Group, PermissionsMixin
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete, pre_delete
from django.utils import timezone

from tags.models import Tag
from utils.models import Vote
# Create your models here.


###  atrributes of a user model:
# username, first_name, last_name, e-mail, password
# groups, user_permissions, is_staff, is_active, is_superuser
# last_login, date_joined
### methods:
# get_username, is_anonyous, is_authenticated, get_full_name, get_short_name
# set_password, check_password, has_perm, has_perms, email_user

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(email, 
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    # user manager
    objects = UserManager()
    # required information 
    email = models.EmailField(verbose_name="email address", db_index=True, max_length=255, unique=True)
    email_verified = models.BooleanField(verbose_name="email verified?", default=False)
    # required to identify the user. 
    USERNAME_FIELD = 'email'
    
    #user_permission = models.ManyToManyField(Permission, null=True, blank=True)
    #group = models.ManyToManyField(Group, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):# __unicode__ on Python 2
        return self.email

    def questions(self):
        return self.mainpost_set.filter(type=0)
        
    def discussions(self):
        return self.mainpost_set.filter(type=1)
        
    def blogs(self):
        return self.mainpost_set.filter(type=2)
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserProfile(models.Model):

    user = models.OneToOneField("User", related_name="user_profile")
    name = models.CharField(verbose_name="user name", max_length=255, null=False, blank=False)
    location = models.CharField(verbose_name="location", max_length=255, blank=True)
    website = models.URLField(blank=True)
    biography = models.TextField(blank=True)
    portrait = models.ImageField(upload_to="user_photo", null=True, blank=True)
    reputation = models.IntegerField(default=1)
    following = models.ManyToManyField('UserProfile',blank=True, related_name = "followers")
    watched_tags = models.ManyToManyField(Tag, blank=True, related_name = "user")
    date_joined = models.DateTimeField(verbose_name="date joined", editable=False)
    last_activity = models.DateTimeField(verbose_name="last activity", null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if not self.date_joined: 
            self.date_joined = timezone.now()
        super(UserProfile, self).save()
            
    def __unicode__(self):
        return self.user.email
    @property
    def follower(self):
        return UserProfile.objects.filter(following__pk = self.pk)
    
    @staticmethod
    def create_user_profile(sender, instance, **kwargs):
        new_user = instance
        new_user_profile, created = UserProfile.objects.get_or_create(user=new_user)
        if created == False: 
            new_user_profile.name = 'user-'+str(new_user_profile.id)
            new_user_profile.save()

    @staticmethod
    def reputation_from_vote(sender, instance, **kwargs):
        content_type = instance.content_type
        obj_id = instance.object_id
        obj = content_type.get_object_for_this_type(pk=obj_id)
        choice = instance.choice
        user_profile = obj.author.user_profile
        user_profile.reputation += choice
        user_profile.save()
    
    @staticmethod
    def reputation_rollback_from_vote(sender, instance, **kwargs):
        content_type = instance.content_type
        obj_id = instance.object_id
        obj = content_type.get_object_for_this_type(pk=obj_id)
        choice = instance.choice
        user_profile = obj.author.user_profile
        user_profile.reputation -= choice
        user_profile.save()    
        
    def get_absolute_url(self):
        return reverse("users:profile-view", kwargs={'pk':self.pk})
    
post_save.connect(UserProfile.create_user_profile, sender=User)
post_save.connect(UserProfile.reputation_from_vote, sender=Vote)
pre_delete.connect(UserProfile.reputation_rollback_from_vote, sender=Vote)