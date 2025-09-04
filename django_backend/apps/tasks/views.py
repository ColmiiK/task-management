from django.views import View
from django.http import JsonResponse


class TaskListPostView(View):
    # with filtering, search, pagination
    def get(self, request):
        return JsonResponse({"message": "test"})

    def post(self, request):
        return JsonResponse({"message": "test"})


class TaskListUpdateDestroy(View):
    def get(self, request, id):
        return JsonResponse({"message": "test"})

    def put(self, request, id):
        return JsonResponse({"message": "test"})

    def patch(self, request, id):
        return JsonResponse({"message": "test"})

    def delete(self, request, id):
        return JsonResponse({"message": "test"})


class TaskAssignView(View):
    def post(self, request, id):
        return JsonResponse({"message": "test"})


class TaskCommentView(View):
    def get(self, request, id):
        return JsonResponse({"message": "test"})

    def post(self, request, id):
        return JsonResponse({"message": "test"})


class TaskHistoryView(View):
    def get(self, request, id):
        return JsonResponse({"message": "test"})
