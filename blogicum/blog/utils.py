from django.db.models import Count, Q
from django.utils import timezone

from .models import Post


def get_posts(user=None, include_unpublished=False):
    """Получение списка публикаций с фильтрацией."""
    now = timezone.now()
    base_queryset = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).annotate(comment_count=Count('comments'))

    if user and user.is_authenticated:
        if include_unpublished:
            queryset = base_queryset.filter(
                Q(is_published=True, category__is_published=True, pub_date__lte=now) |
                Q(author=user)
            )
        else:
            queryset = base_queryset.filter(
                Q(is_published=True, category__is_published=True, pub_date__lte=now) |
                Q(author=user, is_published=True, category__is_published=True, pub_date__lte=now)
            )
    else:
        queryset = base_queryset.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=now
        )

    return queryset.order_by('-pub_date', 'title')