from django.urls import path
from .views import (
    TaskListPostView,
    TaskListUpdateDestroy,
    TaskAssignView,
    TaskCommentView,
    TaskHistoryView,
)


urlpatterns = [
    path("", TaskListPostView.as_view(), name="list-post-task"),
    path("<int:id>/", TaskListUpdateDestroy.as_view(), name="list-update-destroy-task"),
    path("<int:id>/assign/", TaskAssignView.as_view(), name="assign-task"),
    path("<int:id>/comments/", TaskCommentView.as_view(), name="comment-task"),
    path("<int:id>/history/", TaskHistoryView.as_view(), name="history-task"),
]
