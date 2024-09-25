from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Account
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# User registration view
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = email.split('@')[0]


        if Account.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return redirect('accounts:login')

        user = Account.objects.create_user(email=email, username=username, password=password)
        user.is_active = True
        user.save()
        messages.success(request, f"Please check your email ({email}) for activation.")
        current_site = get_current_site(request)
        mail_subject = "Activate your account"
        message = render_to_string('accounts/account_verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        print("mail has been sent")

    return render(request, 'accounts/login.html',  {'active_tab': 'register'} )

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Activation link is invalid.")
        return redirect('accounts:register')

# User login view
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have been logged in successfully!')
            return redirect('accounts:dashboard')  # Ensure this URL exists in your URL patterns
        else:
            messages.error(request, 'Invalid email or password.')
    print("you have been login")
    return render(request, 'accounts/login.html', {'active_tab': 'login'} )

# User logout view
@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    print("you have been")
    return redirect('accounts:login')

def forgotpassword(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject="Reset ur password"
            message=render_to_string('accounts/reset_password_email.html',
                         {'user':user,
                          'domain':current_site,
                          'uidb64':urlsafe_base64_encode(force_bytes(user.pk)),
                          'token':default_token_generator.make_token(user)})
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sennt')
            return redirect('accounts:login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('accounts:forgotpassword')


    return render(request,'accounts/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
       uid=urlsafe_base64_decode(uidb64).decode()
       user=Account._default_manager.get(pk=uid)
    except Exception:
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        user.save()
        messages.success(request,"please reset ur password")
        return redirect('resetpassword')
    else:
        messages.error(request,"link expired")
        return redirect('accounts:login')


def resetpassword(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset is successful')
            return redirect('accounts:login')
        else:
            messages.error(request,'password do not match')
            return redirect('accounts:resetpassword')
    return render(request,'accounts/resetpassword.html')

# User dashboard (profile) view
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})
