from django.views import View
from django.http import JsonResponse


class AuthRegisterView(View):
    def post(self, request):
        return JsonResponse({"message": "test"})


class AuthLoginView(View):
    def post(self, request):
        return JsonResponse({"message": "test"})


class AuthLogoutView(View):
    def post(self, request):
        return JsonResponse({"message": "test"})


class AuthRefreshView(View):
    def post(self, request):
        return JsonResponse({"message": "test"})
