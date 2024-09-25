from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    Form class for users to comment on a post.
    """
    class Meta:
        """
        Meta class to specify the model and form fields for the Comment form.
        """
        model = Comment
        fields = ('body',)