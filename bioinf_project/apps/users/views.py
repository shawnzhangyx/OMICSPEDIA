from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.edit import FormView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import get_current_site
from django.template import loader
from django.http import HttpResponseRedirect

from .models import UserProfile
from posts.models import MainPost
from wiki.models import Page, UserPage
from software.models import Tool
from tags.models import Tag, UserTag
from .forms import UserCreationForm, ProfileForm
# Create your views here.

####  account related views ####
class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserCreationForm
    success_url = '/'

class Login(FormView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    success_url = '/'
    
    def dispatch(self, request):
	if not request.user.is_anonymous(): 
		return HttpResponseRedirect(reverse('index'))
        else: 
            return super(Login, self).dispatch(request)

    def form_valid(self, form):
        login(self.request, form.get_user())
        if 'next' in self.request.GET:
            return redirect(self.request.GET['next'])
        else:
            return super(Login, self).form_valid(form)
            
class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
   
   
   
####  profile related views  ####
class ProfileEdit(UpdateView):
    form_class=ProfileForm
    template_name = "users/profile_edit.html"
    def get_object(self):
        return UserProfile.objects.get(pk=self.kwargs['pk'])
        
        
class ProfileView(DetailView):
    model = UserProfile
    template_name = "users/profile_view.html"
    
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        bookmarks = self.object.user.bookmarks.all()
        # bookmarked posts
        post_bookmarks = bookmarks.filter(content_type=ContentType.objects.get_for_model(MainPost))
        id = post_bookmarks.values_list('object_id',flat=True)
        bookmark_posts = MainPost.objects.filter(id__in = id)
        context['bookmark_posts'] = bookmark_posts
        # bookmarked wiki
        wiki_bookmarks = bookmarks.filter(content_type=ContentType.objects.get_for_model(Page))
        id = wiki_bookmarks.values_list('object_id',flat=True)
        bookmark_wiki = Page.objects.filter(id__in = id)
        context['bookmark_wiki'] = bookmark_wiki
        # bookmarked software
        #software_bookmarks = bookmarks.filter(content_type=ContentType.objects.get_for_model(Tool))
        #id = software_bookmarks.values_list('object_id',flat=True)
        bookmark_software = Tool.objects.filter(page__id__in = id)
        context['bookmark_software'] = bookmark_software
        # tags that the author contributed to 
        #tags_answered = Tag.objects.filter(posts__replies__author = self.object.user).distinct()
        usertags = UserTag.objects.filter(user = self.object.user).order_by('-answer_count')
        context['usertag_list'] = usertags
        userpages = UserPage.objects.filter(user = self.object.user).order_by('-added')
        context['userpage_list'] = userpages
        
        return context
        
class UserListView(ListView):
    model = UserProfile
    template_name = 'users/user_list.html'
    context_object_name = "user_profile_list"
    paginate_by = 30
    
    def get_queryset(self):
        tab = self.request.GET.get('tab')
        if tab == "Reputation":
            return UserProfile.objects.order_by('-reputation')
        elif tab == "Activity":        
            return UserProfile.objects.order_by('-last_activity')
        #elif tab == "Moderators":
            #return UserProfile.objects.filter(user__groups = '')
        else: 
            return UserProfile.objects.order_by('-reputation')
            
    def get_context_data(self,**kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['tab'] = self.request.GET.get('tab')
        return context
    
def email_verification_form(request,sent="no"):
    if request.method == "POST":
        user = request.user
        email_template_name = "users/verification_email.html"
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        use_https = request.is_secure()
        c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
        subject = "Verification the  e-mail address of user "+user.user_profile.name
        content = loader.render_to_string(email_template_name, c)
        send_mail(subject, content, None, [user.email])
        return HttpResponseRedirect(reverse('users:email-verification-form', kwargs={'sent':'sent/'}))
    else:
        return render(request, 'users/email_verification_form.html', {'sent':sent})
    
    
def email_verification_complete(request, uidb64=None, token=None):
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        user.email_verified = True
        user.set_password(user.password)
        user.save()
    else: 
        validlink = False
    return render(request, "users/email_verification_complete.html", {"validlink":validlink})
    
    
class FollowerEditView(UpdateView):
    model = UserProfile
    template_name = "users/follower_list.html"
    fields = []
    
    def form_valid(self, form):
        follower = UserProfile.objects.get(pk=int(self.request.POST.get("follower")))
        if form.instance in follower.following.all():
            follower.following.remove(form.instance)
        else:
            follower.following.add(form.instance)
        follower.save()
        form.instance.save()
        return super(FollowerEditView, self).form_valid(form)
        
class FollowingListView(ListView):
    #model = UserProfile
    template_name = "users/follower_list.html"

    def get_queryset(self):
        return UserProfile.objects.get(pk=self.kwargs['pk']).following.all()
    
    def get_context_data(self,**kwargs):
        context = super(FollowingListView, self).get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(pk=self.kwargs['pk'])
        context['title'] = 'Following'
        return context
    
        
class FollowerListView(ListView):
    model = UserProfile
    template_name = "users/follower_list.html"

    def get_queryset(self):
        return UserProfile.objects.get(pk=self.kwargs['pk']).followers.all()
     
    def get_context_data(self,**kwargs):
        context = super(FollowerListView, self).get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(pk=self.kwargs['pk'])
        context['title'] = 'Followers'

        return context
    