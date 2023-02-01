from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartPageView.as_view(), name="cart"),
    path('add/<int:product_id>/', views.AdddCartView.as_view(), name="add_to_cart"),
    path('delete/<int:product_id>/', views.DeleteProductCartView.as_view(), name="delete_product"),
    path('clear/', views.ClearCartView.as_view(), name="clear_cart"),
]