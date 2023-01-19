from django import forms
from .models import Post
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
