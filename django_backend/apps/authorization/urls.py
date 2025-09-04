from django.urls import path
from .views import (
    AuthRegisterView,
    AuthLoginView,
    AuthLogoutView,
    AuthRefreshView,
)


urlpatterns = [
    path("register/", AuthRegisterView.as_view(), name="auth-register"),
    path("login/", AuthLoginView.as_view(), name="auth-login"),
    path("logout/", AuthLogoutView.as_view(), name="auth-logout"),
    path("refresh/", AuthRefreshView.as_view(), name="auth-refresh"),
]
