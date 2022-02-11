from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField

from src.accounts.models import User


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Article Category"
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.name

    def get_articles(self):
        return Article.objects.filter(category__pk=self.pk)


class ArticleTag(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Article Tag"
        verbose_name_plural = "Article Tags"

    def __str__(self):
        return self.name


class Article(models.Model):
    thumbnail = ResizedImageField(
        upload_to='exarth/images/articles/thumbnail/', null=True, blank=True, quality=100,
        crop=['middle', 'center'],
        size=[250, 250],
        help_text='Take your time and create thumbnail image for your blog '
                  'size must be 250*250 and available format are JPG, JPEG and PNG only.'
    )
    banner_image = ResizedImageField(
        upload_to='exarth/images/articles/banner/', null=True, blank=True, quality=75,
        size=[760, 1024],
        help_text='Banner image will be visible at the top of your article, '
                  'size must be 1024*760 and available format are JPG, JPEG and PNG only.'
    )
    title = models.CharField(
        max_length=255, null=False, blank=False, unique=True,
    )
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True, blank=False)

    description = models.TextField(null=False, blank=False)
    detailed_description = RichTextField(null=False, blank=False)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, null=False, blank=True)
    keywords = models.ManyToManyField(ArticleTag)

    read_time = models.PositiveIntegerField(null=False, blank=False, default=0)
    likes = models.PositiveIntegerField(null=False, blank=False, default=0)
    views = models.PositiveIntegerField(null=False, blank=False, default=0)

    is_active = models.BooleanField(default=True, blank=False, null=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.thumbnail.delete(save=True)
        self.banner_image.delete(save=True)
        super(Article, self).delete(*args, **kwargs)