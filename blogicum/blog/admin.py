from django.contrib import admin

from .helpers import truncate_string
from .models import (
    Category,
    Location,
    Post,
)


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


class PostAdmin(admin.ModelAdmin):
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

    def truncated_text(self, post):
        return truncate_string(post.text, 100)
    truncated_text.short_description = (
        Post._meta.get_field('text').verbose_name
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
