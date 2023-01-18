from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        # нормалізуємо email
        email = self.normalize_email(email)
        # створюємо юзера
        user = self.model(email=email, **extra_fields)
        # хешування пароля
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("Електронна пошта", unique=True)
    profile_img = models.ImageField(upload_to="users/profiles/", blank=True, null=True)
    about = models.TextField("Про себе", null=True, blank=True)
    # null=True працює на рівні бази , а blank=True працює на рівні форми
    instagram = models.URLField(null=True, blank=True)

    USERNAME_FIELD = 'email'  # Яке поле буде використане при логіні
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Юзер"
        verbose_name_plural = "Юзери"

    def __str__(self):
        return self.email
