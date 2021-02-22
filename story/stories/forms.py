from django.conf import settings
from django import forms

from .models import Story

MAX_STORY_LENGTH = settings.MAX_STORY_LENGTH

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_STORY_LENGTH:
            raise forms.ValidationError("This story is too long")
        return content