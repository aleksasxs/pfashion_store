from django import forms
from apps.blog.models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['username', 'email', 'text', 'article', 'is_active']
