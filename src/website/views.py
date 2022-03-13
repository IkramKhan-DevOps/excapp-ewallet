from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, DetailView
from src.website.forms import ArticleFilter
from src.website.models import Article, ArticleTag, ArticleCategory

from src.payments.bll import stripe_connect_account_create


class HomeView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        stripe_connect_account_create()
        return super(HomeView, self).get_context_data(**kwargs)


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

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['article_categories'] = ArticleCategory.objects.all()
        context['article_tags'] = ArticleTag.objects.all()
        context['article_recents'] = Article.objects.all()[:5]

        article_filter = ArticleFilter(self.request.GET, queryset=Article.objects.all())
        context['article_filter_form'] = article_filter.form

        paginator = Paginator(article_filter.qs, 50)
        page_number = self.request.GET.get('page')
        article_page_object = paginator.get_page(page_number)

        context['article_list'] = article_page_object

        return context


class BlogDetailView(DetailView):
    queryset = Article.objects.all()
    template_name = 'website/blog-details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['article_categories'] = ArticleCategory.objects.all()
        context['article_tags'] = ArticleTag.objects.all()
        context['article_recents'] = Article.objects.all()[:5]
        return context


class ComingSoonView(TemplateView):
    template_name = 'website/coming-soon.html'


class LoginView(TemplateView):
    template_name = 'website/sign-in.html'


class SignUpView(TemplateView):
    template_name = 'website/sign-up.html'


class ForgetPasswordView(TemplateView):
    template_name = 'website/forgot.html'
