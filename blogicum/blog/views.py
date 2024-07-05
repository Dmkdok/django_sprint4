from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from .forms import CommentForm, PostForm, ProfileUpdateForm
from .models import Category, Comment, Post
from .utils import get_posts

User = get_user_model()


class PaginateMixin:
    paginate_by = 10


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostQuerysetMixin:
    def get_queryset(self):
        return get_posts(self.request.user)


class CommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class IndexView(PaginateMixin, PostQuerysetMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        queryset = get_posts(user=self.request.user, include_unpublished=True)
        return get_object_or_404(queryset, id=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class CategoryListView(PaginateMixin, PostQuerysetMixin, ListView):
    model = Post
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'post_list'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True)
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileListView(PaginateMixin, ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = (self.model.objects
                    .select_related('author')
                    .filter(author__username=username)
                    .annotate(comment_count=Count('comments'))
                    .order_by('-pub_date'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'])
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user.username])


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        post = self.get_object()
        return redirect('blog:post_detail', post_id=post.id)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.id}
        )


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def handle_no_permission(self):
        post = self.get_object()
        return redirect('blog:post_detail', post_id=post.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class CommentCreateView(CommentMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentDeleteView(CommentMixin, AuthorRequiredMixin, DeleteView):
    pass


class CommentUpdateView(CommentMixin, AuthorRequiredMixin, UpdateView):
    form_class = CommentForm
