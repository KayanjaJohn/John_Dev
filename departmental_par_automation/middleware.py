from django.contrib.auth.middleware import MiddlewareMixin
from django.contrib.auth import logout

class UserStatusCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.user.status == 'Blocked':
                logout(request)
