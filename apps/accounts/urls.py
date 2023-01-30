from django.urls import path

from apps.accounts import views
urlpatterns =[
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('register/', views.UserRegisterView.as_view(), name="register"),
    path('register/done/', views.RegisterDoneView.as_view(), name="register_done"),
    # приймаємо через URL два параметри - uidb64 і token
    path('account/confirm/<uidb64>/<token>/',
         views.activate_account, name='activate_account'),
    path('user_profile/', views.UpdateUserView.as_view(), name="user_profile"),
    path('all_users/', views.AllUsersView.as_view(), name="all_users"),
    path('user_detail/<int:pk>/', views.UserDetailView.as_view(), name="user_detail"),
    path("search/", views.UsersSearchListView.as_view(), name="search_user"),
]