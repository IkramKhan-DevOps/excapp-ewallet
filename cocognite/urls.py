from django.conf.urls import url

from cocognite import settings
from dj_rest_auth.registration.views import VerifyEmailView
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from src.accounts.views import GoogleLoginView, CustomRegisterAccountView
from django.views.static import serve

# from src.website.views import handler404

urlpatterns = [

    # BASE URLS -------------------------------------------------------- #
    path('', include('src.website.urls', namespace='website')),

    # REQUIRED --------------------------------------------------------- #
    path('admin/', admin.site.urls),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    # PORTALS ---------------------------------------------------------- #
    path('a/', include('src.portals.admins.urls', namespace='admin-portal')),
    path('c/', include('src.portals.customer.urls', namespace='moderator-portal')),

    path('', include('src.payments.urls', namespace='payment-stripe')),

    # REST API -------------------------------------------------------------------------------------------
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', CustomRegisterAccountView.as_view(), name='account_create_new_user'),
    # re_path(r'^account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login-view'),

    # path('api/', include('src.api.urls', namespace='api')),

    # NOTIFICATION SERVER ---------------------------------------------- #
    # url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
