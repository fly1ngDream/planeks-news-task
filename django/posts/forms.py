from django import forms
from django.utils import timezone
from datetime import datetime

from pagedown.widgets import PagedownWidget

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    created = forms.DateTimeField(
        initial=datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
        widget=forms.widgets.DateTimeInput(
            format="%m/%d/%Y %H:%M:%S",
            attrs={'placeholder': "DD/MM/YY HH:MM:SS"}
        )
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'attachment',
            'created',
        ]
