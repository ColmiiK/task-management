from django.urls import path

from .views import UserListView, UserDetailView, UserPersonalView


urlpatterns = [
    path("", UserListView.as_view(), name="list-user"),
    path("<int:id>/", UserDetailView.as_view(), name="user-detail"),
    path("me/", UserPersonalView.as_view(), name="user-personal"),
]
