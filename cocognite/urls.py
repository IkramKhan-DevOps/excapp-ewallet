from . import settings
from dj_rest_auth.registration.views import VerifyEmailView
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from src.accounts.views import GoogleLoginView, CustomRegisterAccountView
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
