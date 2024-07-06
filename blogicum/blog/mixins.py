from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse
from django.urls import reverse_lazy

from .helpers import truncate_string
from .models import Comment, Post
from .utils import get_posts


class PaginateMixin:
    paginate_by = 10


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ProfileRedirectMixin():
    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user.username])


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


class TruncatedTextMixin:
    def truncated_text(self, post):
        return truncate_string(post.text, 100)
    truncated_text.short_description = (
        Post._meta.get_field('text').verbose_name
    )
