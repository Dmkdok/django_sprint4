from django.utils import timezone

from .models import Post


def get_posts(category=None, is_published=True):
    """Получение списка публикаций с фильтрацией."""
    queryset = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=is_published,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date', 'title')
    if category:
        queryset = queryset.filter(category=category)
    return queryset
