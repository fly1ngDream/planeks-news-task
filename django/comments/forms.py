from django import forms


from .models import Comment


class CommentForm(forms.Form):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea)
