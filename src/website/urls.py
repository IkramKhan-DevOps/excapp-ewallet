from django.urls import path
from .views import (
    HomeView, Error404View, PrivacyPolicyView, TermsAndConditionsView,
    BlogDetailView, BlogView, ContactView, ComingSoonView, LoginView, SignUpView, ForgetPasswordView,
    SupportView, AboutUsView
)

app_name = "website"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('forget/', ForgetPasswordView.as_view(), name='forget-password'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('support/', SupportView.as_view(), name='support'),
    path('about/', AboutUsView.as_view(), name='about'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('coming-soon/', ComingSoonView.as_view(), name='coming-soon'),
]