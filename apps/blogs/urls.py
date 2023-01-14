from django.urls import path

from apps.blogs.views import IndexPage

urlpatterns = [
    path('', IndexPage.as_view(), name='index')

]