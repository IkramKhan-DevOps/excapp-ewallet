import notifications.urls
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings

urlpatterns = [

    # BASE URLS -------------------------------------------------------- #
    path('', include('src.website.urls', namespace='website')),

    # REQUIRED --------------------------------------------------------- #
    path('admin/', admin.site.urls),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    # PORTALS ---------------------------------------------------------- #
    path('a/', include('src.portals.admins.urls', namespace='admin-portal')),
    path('s/', include('src.portals.student.urls', namespace='student-portal')),
    path('m/', include('src.portals.moderator.urls', namespace='moderator-portal')),

    # NOTIFICATION SERVER ---------------------------------------------- #
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
