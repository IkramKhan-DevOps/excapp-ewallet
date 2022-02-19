from django.urls import path
from .views import CrossAuthView, IdentificationCheckView, UserUpdateView, view_activate

app_name = "accounts"
urlpatterns = [
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth-view'),
    path('identification-check/', IdentificationCheckView.as_view(), name='identification-check'),
    path('user/change/', UserUpdateView.as_view(), name='user-change'),

    path('activate/<uidb64>/<token>/', view_activate, name='activate'),
]
