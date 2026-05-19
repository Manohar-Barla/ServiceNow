import hashlib
import random
from django.utils import timezone
from datetime import timedelta
from .models import OTPVerification

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def track_user_login(request, user):
    """
    Capture IP, User-Agent, and generate a unique device_id.
    Store in UserProfile and update session_key for single-device restriction.
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ip = get_client_ip(request)
    
    # Generate device ID
    device_id_str = f"{user_agent}_{ip}"
    device_id = hashlib.sha256(device_id_str.encode()).hexdigest()
    
    try:
        profile = user.userprofile
        profile.device_id = device_id
        profile.device_details = user_agent
        profile.last_ip = ip
        profile.last_login_time = timezone.now()
        
        if not request.session.session_key:
            request.session.save()
            
        profile.session_key = request.session.session_key
        profile.save()
    except Exception as e:
        print(f"Error tracking login: {e}")

# OTP Placeholder Structure
def generate_otp(user, verification_type):
    code = f"{random.randint(100000, 999999)}"
    OTPVerification.objects.create(
        user=user,
        otp_code=code,
        verification_type=verification_type
    )
    # Placeholder for actual SMS/Email sending logic
    print(f"[MOCK GATEWAY] Sent {verification_type} OTP {code} to {user.username}")
    return code

def verify_otp(user, verification_type, code):
    record = OTPVerification.objects.filter(
        user=user,
        verification_type=verification_type,
        otp_code=code,
        is_verified=False
    ).order_by('-created_at').first()
    
    if record:
        # Check expiry (10 minutes)
        if timezone.now() < record.created_at + timedelta(minutes=10):
            record.is_verified = True
            record.save()
            
            # Update user profile
            profile = user.userprofile
            if verification_type == 'EMAIL':
                profile.is_email_verified = True
            elif verification_type == 'MOBILE':
                profile.is_mobile_verified = True
            profile.save()
            
            return True
    return False

from django.core.mail import send_mail

def alert_whitedevil(subject, message):
    try:
        # For now, print to console/use console backend if configured
        print(f"--- EMAIL TO WHITEDEVIL ---\nSubject: {subject}\n{message}\n---------------------------")
        send_mail(
            subject=subject,
            message=message,
            from_email='security@servicenowcsa.com',
            recipient_list=['whitedevil@example.com'],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending alert: {e}")
