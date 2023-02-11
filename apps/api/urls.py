from django.urls import path
from . import views


from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="FoodieTales API",
        default_version='v1',
        description="FoodieTales API",
        contact=openapi.Contact(email="sultanbek9899@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


urlpatterns = [
    path('docs/', schema_view.with_ui('swagger')),
    path('products/', views.ProductListAPIView.as_view()),
    path('shop/categories/', views.ShopCategoryListAPIView.as_view()),

]