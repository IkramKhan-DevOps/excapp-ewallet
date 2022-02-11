import django_filters
from django.forms import TextInput

from src.website.models import Article


class ArticleFilter(django_filters.FilterSet):

    class Meta:
        model = Article
        fields = {
            'title': ['icontains']
        }