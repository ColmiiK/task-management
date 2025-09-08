from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from apps.users.models import User
from django.contrib.auth import authenticate, login, logout
import json


@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({"success": "CSRF cookie set"})


# username
# password
# confirm_password
# email
class AuthRegister(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data.get("username")
            password = data.get("password")
            confirm_password = data.get("confirm_password")
            email = data.get("email", "")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)
            if password != confirm_password:
                return JsonResponse({"error": "Passwords don't match"}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({"success": f"User {username} registered successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


class AuthLogin(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"success": "Login successful"}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


class AuthLogout(View):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"success": "Logout successful"}, status=200)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)


class AuthRefresh(View):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse(
                {
                    "is_authenticated": True,
                    "username": request.user.username,
                    "email": request.user.email,
                },
                status=200,
            )
        else:
            return JsonResponse({"is_authenticated": False}, status=401)
