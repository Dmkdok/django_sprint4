from django import forms

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите ваш комментарий...'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'location', 'image', 'pub_date')

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок поста'}),
            'text': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Текст поста'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'value': '2023-10-27T10:00'}),
        }