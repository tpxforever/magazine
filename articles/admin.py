from django.contrib import admin
from django.utils import timezone
from .models import Article, Category, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'media_type']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'article_type', 'status', 'featured', 'views', 'created_at']
    list_filter = ['status', 'article_type', 'featured', 'category']
    search_fields = ['title', 'author__username', 'subject_title']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'featured']
    actions = ['publish_articles', 'reject_articles']
    readonly_fields = ['views', 'created_at', 'updated_at']

    def publish_articles(self, request, queryset):
        queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{queryset.count()} article(s) published.')
    publish_articles.short_description = 'Publish selected articles'

    def reject_articles(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} article(s) rejected.')
    reject_articles.short_description = 'Reject selected articles'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'university', 'year_of_study']
