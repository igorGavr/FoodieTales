from django.db import models
from apps.accounts.models import User
from apps.shop.models import Product
# Create your models here.


class Order(models.Model):
    STATUS_NEW = "NEW"
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_REJECTED = "REJECTED"
    STATUS_DELIVERED = "DELIVERED"
    STATUS_ARCHIVED = "ARCHIVED"

    STATUS_CHOICES = (
        (STATUS_NEW, "новий"),
        (STATUS_CONFIRMED,  "підтверджений"),
        (STATUS_REJECTED , "відхилений"),
        (STATUS_DELIVERED , "доставлений"),
        (STATUS_ARCHIVED , "архівований"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.CharField("Адрес", max_length=255)
    mobile = models.CharField("Номер", max_length=15)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created"]

    def __str__(self):
        return f"Номер замовлення #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField("")

    class Meta:
        verbose_name = "Товар Замовлення"
        verbose_name_plural = "Товар Замовлення"
        ordering = ["-quantity"]