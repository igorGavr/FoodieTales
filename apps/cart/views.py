from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from apps.cart.cart import Cart
from apps.shop.models import Product


class CartPageView(TemplateView):
    template_name = "cart.html"


class AdddCartView(View):

    def get(self, request, product_id):
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.add(
            product=product,
            quantity=1
        )
        return redirect("cart")
