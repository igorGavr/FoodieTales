from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from apps.cart.cart import Cart
from apps.order.forms import OrderForm
from apps.shop.models import Product
from django.contrib import messages


class CartPageView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_form"] = OrderForm()
        return context


class AdddCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.add(
            product=product,
            quantity=1
        )
        # передаємо на message фронт
        messages.add_message(request, messages.SUCCESS, "Ваш товар додано в корзину! ")
        return redirect("product_list")


class DeleteProductCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.remove(product)
        return redirect('product_list')


class ClearCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect("product_list")
