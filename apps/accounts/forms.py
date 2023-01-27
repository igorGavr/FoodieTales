from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Електронна пошта",
        # настройки поля
        widget=forms.EmailInput(attrs={"class": "main-input-box", "placeholder": "example@example.com"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "main-input-box"})
    )


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
        ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "profile_img",
            "about",
            "instagram",
        ]
        form_control = {"class": "form-control"}
        widgets={
            "profile_img": forms.FileInput(attrs=form_control),
            "about": forms.TextInput(attrs=form_control),
            "instagram": forms.URLInput(attrs=form_control),
        }
