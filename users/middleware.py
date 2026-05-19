from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.contrib.auth import logout

class RoleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                request.role = request.user.userprofile.role
            except Exception:
                request.role = 'USER'
        else:
            request.role = None

class SecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        is_mobile = any(keyword in user_agent for keyword in ['mobi', 'android', 'iphone', 'ipad', 'ipod'])
        
        # Bypass restrictions for ADMIN and DUMMY
        if getattr(request, 'role', None) in ['ADMIN', 'DUMMY']:
            return None
            
        # Device Restriction: Block mobile
        if is_mobile:
            return HttpResponseForbidden("Mobile devices are not allowed. Please use desktop.")
            
        # Single Device Login Enforcement
        if request.user.is_authenticated and getattr(request, 'role', None) == 'USER':
            try:
                profile = request.user.userprofile
                if profile.session_key and profile.session_key != request.session.session_key:
                    logout(request)
                    return HttpResponseForbidden("Your account was logged in from another device. You have been logged out.")
            except Exception:
                pass
        
        return None

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Allow authenticated users to proceed
        if request.user.is_authenticated:
            return None

        path = request.path_info
        
        # Exact matching login/auth urls
        exempt_urls = [
            reverse('users:login'),
            reverse('users:register'),
            reverse('users:otp_verify'),
        ]
        
        if path in exempt_urls:
            return None
            
        # Match administrative dashboard urls
        if path.startswith('/admin/'):
            return None
            
        # Match static/media files
        if path.startswith(settings.STATIC_URL) or (settings.MEDIA_URL and path.startswith(settings.MEDIA_URL)):
            return None

        # Redirect unauthenticated requests to the login view
        return redirect(reverse('users:login'))

