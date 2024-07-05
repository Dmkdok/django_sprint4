from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'created_at',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
