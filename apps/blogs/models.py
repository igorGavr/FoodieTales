from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField("Назва", max_length=255)
    slug = models.SlugField(max_length=255)
    icon = models.ImageField(upload_to="category/icons/")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField("Назва", max_length=255)
    description = models.TextField("Опис")
    image = models.ImageField("Фото")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    is_draft = models.BooleanField("Черновик", default=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"

    def __str__(self):
        return self.title
