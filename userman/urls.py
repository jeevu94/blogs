from django.urls import path

from . import views

app_name = "userman"

urlpatterns = [
    path(
        "auth/sign-up/",
        views.UserSignUpPageView.as_view(),
        name="user_signup_page_view",
    ),
    path("auth/login/", views.UserLoginPageView.as_view(), name="user_login_page_view"),
    path(
        "auth/logout/",
        views.UserLogoutPageView.as_view(),
        name="user_logout_page_view",
    ),
]
