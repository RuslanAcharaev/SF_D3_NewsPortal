from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            # 'author',
            'title',
            'postCategory',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Текст не должен быть идентичен заголовку."
            )

        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Текст не может быть менее 20 символов."
            })

        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы"
            )
        return title
