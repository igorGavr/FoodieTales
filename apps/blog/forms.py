from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget


# створюємо форму для створення постів
class PostCreateForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = (
            'title',
            'description',
            'image',
            'category',
            'tags',
            'is_draft',
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
            "is_draft": forms.CheckboxInput(attrs={"class": "form-control"}),
        }


# forms.Form - створює форму , але не може зберігати дані в базу напряму
# forms.ModelForm - має звязок з моделю та зберігає дані в базу напряму
# створюємо форму для створення коментів
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", ]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control"})
        }


