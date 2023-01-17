from django.contrib import admin

# Register your models here.
from apps.blog.models import Category, Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # вказуємо які поля ми будемо відображати
    list_display = ["title", "category","created", "is_draft"]
    list_filter = ["category", "is_draft", "created"]
    # додаємо справа вікно для додавання тегів
    filter_horizontal = ["tags"]



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # дасть змогу автоматично заповнювати поле slug
    prepopulated_fields = {"slug":("name",)}
    # вказуємо які поля ми будемо відображати
    list_display = ["name", "slug", "id"]

    