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
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

import StringIO
from PIL import Image

from utils import pagination

from .models import UserProfile, Notification
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

    def get_success_url(self):
        email = self.request.POST.get('email')
        return reverse('users:login')+'?email='+email
    

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
            next = self.request.GET.get('next')
            if next == '/accounts/register/':
                return HttpResponseRedirect(reverse('index'))
            else:
                return redirect(next)
        else:
            return super(Login, self).form_valid(form)
            
    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        if self.request.GET.get('email'):
            email = self.request.GET.get('email')
            context['message'] = 'Congratulations, your email '+ email +' has been succesfully registered. Log in to your account.'
        return context
        
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
        
    def form_valid(self, form):
        image_field = form.cleaned_data.get('portrait')
        image_file = StringIO.StringIO(image_field.read())
        image = Image.open(image_file)
        SIZE = 400,400
        image = image.resize(SIZE, Image.ANTIALIAS)
        image_file = StringIO.StringIO()
        image.save(image_file, 'JPEG', quality=90)
        image_field.file = image_file
        return super(ProfileEdit,self).form_valid(form)
    
class ProfileView(DetailView):
    model = UserProfile
    template_name = "users/profile_view.html"
    
    
    def get_context_data(self, **kwargs):
        page_limit = 20
        context = super(ProfileView, self).get_context_data(**kwargs)
        tab = self.request.GET.get('tab')
        if not tab: 
            tab = "Summary" 
        mark = self.request.GET.get('mark')
        if not mark:
            mark = 'posts'
        page = self.request.GET.get('page')
        # 1. questions 
        questions = self.object.user.questions()
        # 2. answers
        answers = self.object.user.replypost_set.all()
        # 3. discussions
        discussions = self.object.user.discussions()
        # 4. blogs 
        blogs = self.object.user.blogs()
        # 5. bookmarks
        bookmarks = self.object.user.bookmarks.all()
        # bookmarked posts
        post_bookmarks = bookmarks.filter(content_type=ContentType.objects.get_for_model(MainPost))
        id = post_bookmarks.values_list('object_id',flat=True)
        bookmark_posts = MainPost.objects.filter(id__in = id)
        # bookmarked wiki
        wiki_bookmarks = bookmarks.filter(content_type=ContentType.objects.get_for_model(Page))
        id = wiki_bookmarks.values_list('object_id',flat=True)
        bookmark_wiki = Page.objects.filter(id__in = id)
        bookmark_software = Tool.objects.filter(page__id__in = id)
        # tags that the author contributed to 
        usertags = UserTag.objects.filter(user = self.object.user).order_by('-answer_count')
        # wikis that authors contribute to. 
        userpages = UserPage.objects.filter(user = self.object.user, edits__gt = 0).order_by('-added')
        # list count 
        question_count = questions.count()
        answer_count = answers.count()
        discussion_count = discussions.count()
        blog_count = blogs.count()
        bookmark_count = bookmarks.count()+bookmark_software.count()
        bookmark_wiki_count = bookmark_wiki.count()
        bookmark_post_count = bookmark_posts.count()
        bookmark_software_count = bookmark_software.count()
        usertag_count = usertags.count()
        userpage_count = userpages.count()
        # paginate the list 
        question_list = pagination(questions, page, page_limit)
        answer_list = pagination(answers, page, page_limit)
        discussion_list = pagination(discussions, page, page_limit)
        blog_list = pagination(blogs, page, page_limit)
        bookmark_post_list = pagination(bookmark_posts, page, page_limit)
        bookmark_wiki_list = pagination(bookmark_wiki, page, page_limit)
        bookmark_software_list = pagination(bookmark_software, page, page_limit)
        usertag_list = pagination(usertags, page, page_limit)
        userpage_list = pagination(userpages, page, page_limit)
        tab_list_dict = {'Questions':question_list, 'Answers':answer_list,'Discussions':discussion_list, 'Blogs':blog_list, 'Bookmarks':{'wiki':bookmark_wiki,'posts':bookmark_posts, 'software':bookmark_software}, 'Tags':usertag_list,'Wiki':userpage_list, 'Summary':False,  '':False}
        page_obj = tab_list_dict[tab]
        # if page obj is one of the bookmark. 
        if tab == 'Bookmarks':
            page_obj = page_obj[mark]
        # adding the list to the context. 
        context['tab'] = tab
        context['mark'] = mark
        context['page_obj'] = page_obj
        context['questions'] = question_list
        context['answers'] = answer_list
        context['discussions'] = discussion_list
        context['blogs'] = blog_list 
        context['bookmark_posts'] = bookmark_post_list
        context['bookmark_wiki'] = bookmark_wiki_list
        context['bookmark_software'] = bookmark_software_list
        context['usertag_list'] = usertag_list
        context['userpage_list'] = userpage_list
        # list count
        context['question_count'] = question_count
        context['answer_count'] = answer_count
        context['discussion_count'] = discussion_count
        context['blog_count'] = blog_count
        context['bookmark_count'] = bookmark_count
        context['bookmark_wiki_count'] = bookmark_wiki_count
        context['bookmark_post_count'] = bookmark_post_count
        context['bookmark_software_count'] = bookmark_software_count
        context['usertag_count'] = usertag_count
        context['userpage_count'] = userpage_count
        if page_obj != False:
            context['is_paginated']=True
 
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
            return UserProfile.objects.order_by('-last_activity')
            
    def get_context_data(self,**kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['tab'] = self.request.GET.get('tab') or 'Activity'
        return context
    
@login_required
def email_verification_form(request,sent=""):
    if request.user.email_verified:
        return HttpResponseRedirect('/')
    
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
        # add the user to the verified group
        group = Group.objects.get(name = 'verified_users')
        user.groups.add(group)
        #resaving the password will change the token
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

class NotificationListView(ListView):
    #model = Notification
    template_name = "users/notification_list.html"
    context_object_name = 'notification_list'
    
    def get_queryset(self):
        type = self.kwargs['type']
        if type =='all':
            return Notification.objects.filter(user__id = self.kwargs['pk']).order_by('-created')
        elif type == 'unread':
            return Notification.objects.filter(user__id = self.kwargs['pk'], unread = True).order_by('-created')
            
    def get_context_data(self):
        context = super(NotificationListView, self).get_context_data()
        context['unread_count'] = Notification.objects.filter(user__id = self.kwargs['pk'], unread = True).count()
        context['total_count'] = Notification.objects.filter(user__id = self.kwargs['pk']).count()
        return context
        
        
def read_notification(request):
    pk = int(request.POST['pk'])
    notification = Notification.objects.get(pk=pk)
    notification.unread = False
    notification.save()
    return HttpResponse('1')
    
