from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from src.accounts.forms import UserProfileForm

from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import permissions, status
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from cocognite.settings import GOOGLE_CALLBACK_ADDRESS
from src.accounts.models import User
from src.accounts.serializers import CustomRegisterAccountSerializer
from src.accounts.tokens import account_activation_token



@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):

    def get(self, request):

        if request.user.is_superuser:
            return redirect('admin-portal:dashboard')
        else:
            return redirect('customer-portal:dashboard')


@method_decorator(login_required, name='dispatch')
class IdentificationCheckView(View):

    def get(self, request):

        # IS USER ALREADY IDENTIFIED
        if request.user.is_completed: return redirect('accounts:cross-auth-view')
        return render(request, 'accounts/identification-check.html')

    def post(self, request):

        # IF USER ALREADY IDENTIFIED
        if request.user.is_completed: return redirect('accounts:cross-auth-view')

        user_type = request.POST.get('user_type', None)

        # IF USER HAS TYPE
        if user_type is not None:
            user = request.user

            # IF USER HAS CORRECT TYPE
            if user_type == 's' or user_type == 'm' or user_type == 'p':
                if user_type == 's':
                    messages.success(request, "You are identified as Student")
                    user.is_student = True
                elif user_type == 'm':
                    messages.success(request, "You are identified as Moderator")
                    user.is_moderator = True
                else:
                    messages.success(request, "You are identified as Parent")
                    user.is_parent = True
                user.is_completed = True
                user.save()
                return redirect('accounts:cross-auth-view')
            else:
                messages.error(request, "Please provide correct user type")
        else:
            messages.error(request, "Please provide user type")

        return render(request, 'accounts/identification-check.html')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = GOOGLE_CALLBACK_ADDRESS


class CustomRegisterAccountView(APIView):
    serializer_class = CustomRegisterAccountSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = {}
        status_code = status.HTTP_400_BAD_REQUEST
        serializer = CustomRegisterAccountSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=False)
            data = {'success': 'Account created successfully'}
            status_code = status.HTTP_201_CREATED

            current_site = get_current_site(request)
            mail_subject = 'Activate your TaskTok account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

        else:
            data = serializer.errors
        return Response(data=data, status=status_code)


def view_activate(request, uidb64, token):
    try:

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        try:
            email_account = EmailAddress.objects.get(user=user)
        except EmailAddress.DoesNotExist:
            email_account = EmailAddress.objects.create(
                user=user, email=user.email, primary=True
            )
        email_account.verified = True
        email_account.save()

        user.save()
        # return redirect('home')
        return render(
            request,
            template_name='accounts/signup_confirm.html',
            context={
                'message': 'Thank you for your email confirmation, GOOD LUCK! help the needy, make your '
                           'profile, be a reason of someone to smile and become a HERO.'
            }
        )
    else:
        return render(
            request,
            template_name='accounts/signup_confirm.html',
            context={'message': 'unable to activate account because the activation link is invalid'}
        )