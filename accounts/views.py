from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from django.core.mail import EmailMessage, send_mail
from website import settings
from django.views.generic import View
from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utiliz import token_generator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView as password_view


class PasswordChangeView(password_view):
    form_class = PasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy("index:home")


# Register
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('accounts:activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

            activate_url = "http://%s%s" % (domain, link)
            email_subject = 'Activate your account'
            email_body = 'Hi %s please use this link to verify your account\n%s' % (user.username, activate_url)
            email_message = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user]
            )

            email_message.send(fail_silently=False)
            messages.success(request, 'Account successful created, please verify your account.',
                           extra_tags='register_success')
            return redirect('accounts:login')
    else:
        form = RegisterForm(None)
    return render(request, 'accounts/register.html', {'form': form})


# Profile page
@login_required
def userProfile(request, slug=None):
    profile = None
    try:
        profile = Profile.objects.get(user__slug=slug)
    except:
        return redirect('accounts:index_404')
    return render(request, 'accounts/profile.html', {'profile': profile})


def page_not_found(request):
    return render(request, 'accounts/index_404.html', {'obj': request})


# Login
class Login(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:profile', args=[self.request.user.slug])

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'email or password are invalid. please try again.', extra_tags='validate_form')
        return redirect('accounts:login')


# Logout
class Logout(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('accounts:login')


def user_activated(request):
    user = User.objects.get(id=request.user.id)

    if user:
        user.user_signed = True
        user.save()


class Verification(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not token_generator.check_token(user, token):
                return redirect('accounts:login')

            if user.is_active:
                user_activated(request)
                return redirect('accounts:login')
            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully", extra_tags='register_success')
            return redirect('accounts:login_success')
        except:
            pass
