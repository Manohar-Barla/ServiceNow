from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .forms import RegisterForm, LoginForm
from .models import LoginHistory, AdminActionLog, LoginAttempt, UserProfile
from .utils import track_user_login, alert_whitedevil, get_client_ip
import random

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email', '')
            user.save()
            
            # For standard registers, let's treat them like regular login (require OTP approval)
            otp_code = str(random.randint(100000, 999999))
            ip = get_client_ip(request)
            ua = request.META.get('HTTP_USER_AGENT', '')
            
            LoginAttempt.objects.create(
                user=user, otp_code=otp_code, ip_address=ip, device_details=ua
            )
            LoginHistory.objects.create(
                user=user, status='PENDING_APPROVAL_REGISTER', ip_address=ip, device_details=ua
            )
            
            msg = f"New Registration Attempt by {user.username} ({user.email})\nIP: {ip}\nDevice: {ua}\nOTP CODE: {otp_code}\n\nApprove via Dashboard or send this code to the user."
            alert_whitedevil(f"New Registration: {user.username}", msg)
            
            request.session['pending_user_id'] = user.id
            messages.info(request, "Registration successful. Pending administrator OTP approval.")
            return redirect('users:otp_verify')
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                ip = get_client_ip(request)
                ua = request.META.get('HTTP_USER_AGENT', '')
                
                # Check user role
                role = getattr(user.userprofile, 'role', 'USER')
                
                if role == 'USER':
                    # Generate OTP and require approval
                    otp_code = str(random.randint(100000, 999999))
                    LoginAttempt.objects.create(
                        user=user, otp_code=otp_code, ip_address=ip, device_details=ua
                    )
                    LoginHistory.objects.create(
                        user=user, status='PENDING_APPROVAL', ip_address=ip, device_details=ua
                    )
                    
                    msg = f"New Login Attempt by {user.username} ({user.email})\nIP: {ip}\nDevice: {ua}\nOTP CODE: {otp_code}\n\nApprove via Dashboard or send this code to the user."
                    alert_whitedevil(f"New Login Attempt: {user.username}", msg)
                    
                    request.session['pending_user_id'] = user.id
                    return redirect('users:otp_verify')
                else:
                    # WhiteDevil or Dummy User (no restriction)
                    login(request, user)
                    track_user_login(request, user)
                    LoginHistory.objects.create(
                        user=user, status='SUCCESS', ip_address=ip, device_details=ua
                    )
                    messages.info(request, f"Welcome back, {username}!")
                    next_url = request.POST.get('next') or request.GET.get('next') or 'dashboard:index'
                    return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    # Log the session out properly
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            profile.session_key = None
            profile.save()
        except Exception:
            pass
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

def otp_verify_view(request):
    pending_user_id = request.session.get('pending_user_id')
    if not pending_user_id:
        return redirect('users:login')
        
    user = get_object_or_404(User, id=pending_user_id)
    attempt = LoginAttempt.objects.filter(user=user, is_approved=False).order_by('-created_at').first()
    
    if not attempt:
        # Check if it was approved in the background by WhiteDevil
        last_attempt = LoginAttempt.objects.filter(user=user, is_approved=True).order_by('-created_at').first()
        if last_attempt:
            login(request, user)
            track_user_login(request, user)
            del request.session['pending_user_id']
            
            # Record log
            LoginHistory.objects.create(
                user=user, status='SUCCESS', ip_address=last_attempt.ip_address, device_details=last_attempt.device_details
            )
            
            messages.success(request, "Your login has been approved by the administrator.")
            return redirect('dashboard:index')
        return redirect('users:login')

    if request.method == 'POST':
        otp_input = request.POST.get('otp', '').strip()
        if otp_input == attempt.otp_code:
            attempt.is_approved = True
            attempt.save()
            
            login(request, user)
            track_user_login(request, user)
            del request.session['pending_user_id']
            
            LoginHistory.objects.create(
                user=user, status='SUCCESS', ip_address=attempt.ip_address, device_details=attempt.device_details
            )
            
            messages.success(request, "Login verified successfully.")
            return redirect('dashboard:index')
        else:
            messages.error(request, "Invalid OTP code.")
            
    return render(request, 'users/otp_verify.html', {'email': user.email})

def is_whitedevil_only(user):
    return user.is_authenticated and user.username == 'WhiteDevil'

@user_passes_test(is_whitedevil_only, login_url='home')
def whitedevil_dashboard_view(request):
    # Active Sessions (Profiles with non-empty session_key)
    active_profiles = UserProfile.objects.exclude(session_key__isnull=True).exclude(session_key='')
    pending_logins = LoginAttempt.objects.filter(is_approved=False).order_by('-created_at')
    login_history = LoginHistory.objects.all().order_by('-created_at')[:50]
    action_logs = AdminActionLog.objects.all().order_by('-timestamp')[:50]
    
    return render(request, 'users/whitedevil_dashboard.html', {
        'active_profiles': active_profiles,
        'pending_logins': pending_logins,
        'login_history': login_history,
        'action_logs': action_logs
    })

@user_passes_test(is_whitedevil_only, login_url='home')
def admin_approve_login(request, attempt_id):
    attempt = get_object_or_404(LoginAttempt, id=attempt_id)
    attempt.is_approved = True
    attempt.save()
    
    AdminActionLog.objects.create(
        admin_user=request.user,
        target_user=attempt.user,
        action='LOGIN_APPROVAL',
        details=f"Approved login attempt from IP {attempt.ip_address}"
    )
    messages.success(request, f"Approved login for {attempt.user.username}.")
    return redirect('users:whitedevil_dashboard')

@user_passes_test(is_whitedevil_only, login_url='home')
def admin_reset_device(request, user_id):
    target = get_object_or_404(User, id=user_id)
    profile = target.userprofile
    old_id = profile.device_id
    profile.device_id = None
    profile.session_key = None
    profile.save()
    
    AdminActionLog.objects.create(
        admin_user=request.user,
        target_user=target,
        action='DEVICE_RESET',
        details=f"Reset device lock. Old ID: {old_id}"
    )
    messages.success(request, f"Reset device lock for {target.username}.")
    return redirect('users:whitedevil_dashboard')

@user_passes_test(is_whitedevil_only, login_url='home')
def admin_terminate_session(request, user_id):
    target = get_object_or_404(User, id=user_id)
    profile = target.userprofile
    if profile.session_key:
        Session.objects.filter(session_key=profile.session_key).delete()
        profile.session_key = None
        profile.save()
        
        AdminActionLog.objects.create(
            admin_user=request.user,
            target_user=target,
            action='USER_TERMINATION',
            details="Forcefully terminated user session"
        )
        messages.success(request, f"Terminated session for {target.username}.")
    else:
        messages.warning(request, f"No active session found for {target.username}.")
    return redirect('users:whitedevil_dashboard')
