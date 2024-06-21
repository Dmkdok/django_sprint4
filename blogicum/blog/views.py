from django.shortcuts import (
    render,
    get_object_or_404
)

from .models import Category
from .utils import get_posts


def index(request):
    """Обрабатывает запросы к главной странице блога."""
    post_list = get_posts()[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    """Обрабатывает запросы к странице детализации поста."""
    post = get_object_or_404(get_posts(), id=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Обрабатывает запросы к странице категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    context = {'category': category,
               'post_list': get_posts(category=category)}
    return render(request, 'blog/category.html', context)
