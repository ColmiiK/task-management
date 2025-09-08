from django.views import View
from django.http import JsonResponse
from apps.users.models import User
from django.core.paginator import Paginator
import json


class UserListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        users = User.objects.all().order_by("id")
        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("page_size", 10))

        paginator = Paginator(users, per_page)
        page_obj = paginator.get_page(page)

        user_list = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            for user in page_obj
        ]

        return JsonResponse(
            {
                "users": user_list,
                "total_pages": paginator.num_pages,
                "current_page": page_obj.number,
                "total_users": paginator.count,
            }
        )


class UserDetailView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            user = User.objects.get(pk=id)
            return JsonResponse(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            )
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    def put(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        try:
            user = User.objects.get(pk=id)
            user.username = data.get("username", user.username)
            user.email = data.get("email", user.email)
            user.save()
            return JsonResponse(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            )
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)


class UserPersonalView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        user = request.user
        return JsonResponse(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        )
