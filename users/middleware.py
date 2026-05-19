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
