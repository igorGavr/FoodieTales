from django.shortcuts import render
from django.views.generic import ListView

from apps.shop.models import Product


class ProductListView(ListView):
    template_name = "product_list.html"
    model = Product
    queryset = Product.objects.filter(is_available=True)
