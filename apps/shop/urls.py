from django.urls import path
from apps.shop import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
]