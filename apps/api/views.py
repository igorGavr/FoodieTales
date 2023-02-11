from django.shortcuts import render
from rest_framework.generics import ListAPIView
# Create your views here.
from .serializers import ProductSerializer, ShopCategorySerializer
from apps.shop.models import Product, ShopCategory


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_available=True)


class ShopCategoryListAPIView(ListAPIView):
    serializer_class = ShopCategorySerializer
    queryset = ShopCategory.objects.all()
