from .cart import Cart


# створюємо контекст
def get_cart(request):
    cart = Cart(request)
    return {"cart": cart}
