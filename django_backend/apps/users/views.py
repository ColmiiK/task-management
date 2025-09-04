from django.views import View
from django.http import JsonResponse


class UserListView(View):
    # list with pagination
    def get(self, request):
        return JsonResponse({"message": "test"})


class UserDetailView(View):
    def get(self, request, id):
        return JsonResponse({"method": "GET" + str(id)})

    def put(self, request, id):
        return JsonResponse({"method": "PUT"})


class UserPersonalView(View):
    def get(self, request):
        return JsonResponse({"method": "GET"})
