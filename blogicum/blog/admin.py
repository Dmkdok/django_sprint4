from django.contrib import admin

from .mixins import TruncatedTextMixin
from .models import Category, Comment, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'is_published',
        'created_at'
    )
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description')
    list_per_page = 20


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at'
    )
    list_filter = ('is_published', 'created_at')
    search_fields = ('name',)
    list_per_page = 20


class PostAdmin(TruncatedTextMixin, admin.ModelAdmin):
    list_display = (
        'title',
        'truncated_text',
        'pub_date', 'author',
        'location'
    )
    list_filter = (
        'is_published',
        'created_at',
        'pub_date',
        'author',
        'location',
        'category'
    )
    search_fields = ('title', 'text')
    list_per_page = 20


class CommentAdmin(TruncatedTextMixin, admin.ModelAdmin):
    list_display = ('author', 'post', 'truncated_text', 'created_at')
    list_filter = ('created_at', 'author', 'post')
    search_fields = ('text', 'author', 'post')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
