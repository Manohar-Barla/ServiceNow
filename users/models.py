from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('DUMMY', 'Dummy'),
        ('USER', 'User'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    
    # Auto Profile Creation & Tracking Fields
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    device_details = models.TextField(blank=True, null=True)
    last_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_time = models.DateTimeField(blank=True, null=True)
    session_key = models.CharField(max_length=255, blank=True, null=True)
    
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class OTPVerification(models.Model):
    TYPE_CHOICES = [
        ('EMAIL', 'Email'),
        ('MOBILE', 'Mobile'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    verification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.verification_type} - {self.otp_code}"

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50) # SUCCESS, FAILED, DEVICE_MISMATCH
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    device_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.status}"

class AdminActionLog(models.Model):
    admin_user = models.ForeignKey(User, related_name='actions_made', on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, related_name='actions_received', on_delete=models.CASCADE)
    action = models.CharField(max_length=50) # DEVICE_RESET, LOGIN_APPROVAL, USER_TERMINATION
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    device_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
