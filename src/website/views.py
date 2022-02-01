from django.views.generic import TemplateView, ListView


class HomeView(TemplateView):
    template_name = 'website/home.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'website/policy.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'website/terms.html'


class ContactView(TemplateView):
    template_name = 'website/contact.html'


class SupportView(TemplateView):
    template_name = 'website/support.html'


class AboutUsView(TemplateView):
    template_name = 'website/about-us.html'


class Error404View(TemplateView):
    template_name = 'website/404.html'


class BlogView(TemplateView):
    template_name = 'website/blog.html'


class BlogDetailView(TemplateView):
    template_name = 'website/blog-details.html'


class ComingSoonView(TemplateView):
    template_name = 'website/coming-soon.html'


class LoginView(TemplateView):
    template_name = 'website/sign-in.html'


class SignUpView(TemplateView):
    template_name = 'website/sign-up.html'


class ForgetPasswordView(TemplateView):
    template_name = 'website/forgot.html'
