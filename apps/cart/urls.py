from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartPageView.as_view(), name="cart"),
    path('add/<int:product_id>/', views.AdddCartView.as_view(), name="add_to_cart"),
]