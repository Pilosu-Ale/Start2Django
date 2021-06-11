from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)

    def clean_title(self):
        title = self.cleaned_data['title']
        if "hack" in title.lower():
            raise forms.ValidationError("You has typed an illegal word")
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if "hack" in content.lower():
            raise forms.ValidationError("You has typed an illegal word")
        return content