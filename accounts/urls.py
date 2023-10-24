from django.urls import path
from .views import (
    UserListView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    user_detail,
    user_list,
)


app_name = "accounts"


urlpatterns = [
    path("users/", user_list, name="list_users"),
    path("users/<int:pk>/", user_detail, name="user_info"),
    path("users/register/", UserRegisterView.as_view(), name="user_register"),
    path("users/login/", UserLoginView.as_view(), name="user_login"),
    path("users/logout/", UserLogoutView.as_view(), name="user_logout"),
]
