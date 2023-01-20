from django.urls import path

from apps.blog import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name="index"),
    path('products/', views.ProductsView.as_view(), name="products"),
    path('category/list/',views.CategoryListView.as_view(), name="category_list"),
    path('post/list/', views.PostListView.as_view(), name="post_list"),
    # робимо фільтрацію
    path(
        'post/list/<slug:category_slug>/',
        views.PostListView.as_view(),
        name="post_category_list"
         ),
    # вивід окремого поста
    path('post/detail/<int:pk>/',views.PostDetailView.as_view(), name="post_detail"),
    # створення поста
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    # отримання всіх постів юзера
    path('post/author/list/', views.AuthorPostsListView.as_view(), name="author_posts"),
    # видалення поста
    path('post/delete/<int:pk>/', views.delete_author_post, name="post_delete"),
    # деактивація поста
    path('post/deactivate/<int:pk>', views.deactivate_author_post, name="deactivate_post"),
    # активація поста
    path('post/activate/<int:pk>', views.activate_author_post, name="activate_post"),
    # апдейт поста
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name="update_post"),
    # створення комента
    path('comment/create/<int:post_id>/', views.CommentCreateView.as_view(), name="create_comment"),

]