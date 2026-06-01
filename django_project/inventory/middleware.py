from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith(settings.STATIC_URL) and not request.path.startswith(settings.MEDIA_URL):
            # Allow access to the login page itself
            login_url = reverse('login')
            if request.path != login_url:
                if not request.user.is_authenticated or not request.user.is_superuser:
                    return redirect(f"{login_url}?next={request.path}")
                    
        response = self.get_response(request)
        return response
