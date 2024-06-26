from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Category, Post
from .utils import get_posts
from django.contrib.auth import get_user_model

User = get_user_model()

class PaginateMixin:
    paginate_by = 10

class ProfileListView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['user_posts'] = get_posts().filter(author=profile_user)
        context['is_owner'] = self.request.user == profile_user
        return context

class IndexView(PaginateMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return get_posts()[:5]

class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(get_posts(), id=post_id)

class CategoryPostsView(PaginateMixin, ListView):
    template_name = 'blog/category.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return get_posts(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileView(PaginateMixin, DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['user_posts'] = get_posts().filter(author=profile_user)
        context['is_owner'] = self.request.user == profile_user
        return context
