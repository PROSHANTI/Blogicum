from django import forms
from django.contrib.auth.models import User

from blog.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S',
                                            attrs={'type': 'datetime-local'})
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'cols': 5, 'rows': 5})
        }
