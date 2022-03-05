from django.conf.urls import url
from django.views.generic import TemplateView

from cocognite import settings
from dj_rest_auth.registration.views import VerifyEmailView
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from src.accounts.views import GoogleLoginView, CustomRegisterAccountView
from django.views.static import serve

urlpatterns = [
    path('', include('src.website.urls', namespace='website')),
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
    path('500/', TemplateView.as_view(template_name='500.html'), name='500'),
]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    path('', include('src.payments.urls', namespace='payment-stripe')),
    path('a/', include('src.portals.admins.urls', namespace='admin-portal')),
    path('c/', include('src.portals.customer.urls', namespace='moderator-portal')),
    path('api/', include('src.api.urls', namespace='api')),
    # url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

urlpatterns += [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', CustomRegisterAccountView.as_view(), name='account_create_new_user'),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login-view'),
    # re_path(r'^account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
