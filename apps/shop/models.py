from django.db import models


# Create your models here.

# Категорія товару
class ShopCategory(models.Model):
    name = models.CharField("Назва", max_length=50)
    slug = models.SlugField(max_length=70)

    class Meta:
        verbose_name = "Категорія товару"
        verbose_name_plural = "Категорії товарів"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Назва", max_length=255)
    description = models.TextField("Опис")
    price = models.DecimalField("Ціна", max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        ShopCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )
    is_available = models.BooleanField("Доступно", default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ["-created"]

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="product/images/")

    def __str__(self):
        return self.product.name