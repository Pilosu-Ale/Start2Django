from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)

    def _clean_form(self):
        title = self.cleaned_data['title']
        content = self.cleaned_data['content']
        if "hack" in title:
            raise forms.ValidationError("You has typed an illegal word!")
        if "hack" in content:
            raise forms.ValidationError("You has typed an illegal word!")