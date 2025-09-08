from django.urls import path

from .views import csrf_token, AuthRegister, AuthLogin, AuthLogout, AuthRefresh


urlpatterns = [
    path("auth/csrf/", csrf_token),
    path("auth/register/", AuthRegister.as_view(), name="auth-register"),
    path("auth/login/", AuthLogin.as_view(), name="auth-login"),
    path("auth/logout/", AuthLogout.as_view(), name="auth-logout"),
    path("auth/refresh/", AuthRefresh.as_view(), name="auth-refresh"),
]
