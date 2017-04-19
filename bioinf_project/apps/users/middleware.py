from django.utils import timezone
from .models import UserProfile


class UpdateLastActivityMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if request.user.is_authenticated():
            UserProfile.objects.filter(user__id=request.user.id) \
                           .update(last_activity=timezone.now())