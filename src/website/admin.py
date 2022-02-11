from django.contrib import admin
from django.utils.html import format_html
from src.website.models import Article, ArticleCategory, ArticleTag


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description']


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category', 'author', 'read_time', 'likes', 'views', 'is_active', 'created_on']
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        ('Content', {'fields': ('detailed_description', )}),
        ('Media', {'fields': ('thumbnail', 'banner_image')}),
        ('Details', {'fields': ('category', 'posted_by', 'keywords')}),
        ('Statistics', {
            'fields': (
                'read_time', 'likes', 'views'
            ),
        }),
        ('Permissions', {
            'fields': (
                'is_active',
            ),
        }),
    )

    def author(self, obj):
        return format_html(
            '<a href="/admin/accounts/user/{}/change/">{}</a>',
            obj.posted_by.pk, obj.posted_by.username
        )


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)