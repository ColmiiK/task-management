from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from apps.tasks.models import Task, TaskAssigment, TaskHistory
from apps.users.models import User
from apps.common.models import Comment


def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date,
        "estimated_hours": float(task.estimated_hours),
        "actual_hours": float(task.actual_hours) if task.actual_hours else None,
        "created_by": task.created_by.username,
        "assigned_to": [user.username for user in task.assigned_to.all()],
        "tags": [tag.name for tag in task.tags.all()],
        "parent_task": task.parent_task_id,
        "metadata": task.metadata,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }


class TaskListPostView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        tasks = Task.object.all()

        search = request.GET.get("search")
        priority = request.GET.get("priority")
        status = request.GET.get("status")

        if status:
            tasks = Task.filter(status=status)
        if priority:
            tasks = Task.filter(priority=priority)
        if search:
            tasks = Task.filter(Q(title__icontains=search) | Q(description__icontains=search))

        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("page_size", 10))
        paginator = Paginator(tasks.order_by("-created_at"), per_page)
        page_obj = paginator.get_page(page)

        return JsonResponse(
            {
                "tasks": [serialize_task(task) for task in page_obj],
                "total_pages": paginator.num_pages,
                "current_page": page_obj.number,
                "total_users": paginator.count,
            }
        )

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        title = data.get("title")
        description = data.get("description", "")
        status = data.get("status")
        priority = data.get("priority")
        due_date = data.get("due_date")
        estimated_hours = data.get("estimated_hours")
        actual_hours = data.get("actual_hours")
        metadata = data.get("metadata", {})
        parent_task_id = data.get("parent_task")

        if not title or not status or not priority or not due_date or not estimated_hours:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        task = Task.objects.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            estimated_hours=estimated_hours,
            actual_hours=actual_hours,
            metadata=metadata,
            parent_task_id=parent_task_id,
            created_by=request.user,
        )
        assigned_to_ids = data.get("assigned_to", [])
        tag_ids = data.get("tags", [])

        if assigned_to_ids:
            task.assigned_to.set(assigned_to_ids)
        if tag_ids:
            task.tags.set(tag_ids)

        return JsonResponse(serialize_task(task), status=201)


class TaskListUpdateDestroy(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        try:
            task = Task.objects.get(id=id)
            return JsonResponse(serialize_task(task))
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

    def put(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "estimated_hours",
            "actual_hours",
            "metadata",
            "parent_task",
        ]
        for field in fields:
            setattr(task, field, data.get(field, getattr(task, field)))
        task.save()
        if "assigned_to" in data:
            task.assigned_to.set(data["assigned_to"])
        if "tags" in data:
            task.tags.set(data["tags"])

    def patch(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "estimated_hours",
            "actual_hours",
            "metadata",
            "parent_task",
        ]
        for field in fields:
            if field in data:
                setattr(task, field, data.get(field, getattr(task, field)))
        task.save()
        if "assigned_to" in data:
            task.assigned_to.set(data["assigned_to"])
        if "tags" in data:
            task.tags.set(data["tags"])

    def delete(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return JsonResponse({"success": "Task archived"})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)


class TaskAssignView(View):
    def post(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

        try:
            data = json.loads(request.body)
            user_ids = data.get("assigned_to", [])
            task.assigned_to.set(user_ids)

            TaskAssignment.objects.filter(task=task).delete()
            for uid in user_ids:
                user = User.objects.get(pk=uid)
                TaskAssignment.objects.create(task=task, user=user, assigned_by=request.user)

            TaskHistory.objects.create(
                task=task,
                user=request.user,
                action="Assigned users",
                old_value="N/A",
                new_value=f"User IDs: {user_ids}",
            )
            return JsonResponse({"success": "Users assigned", "assigned_to": user_ids}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)


class TaskCommentView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

        comments = task.comments.filter(is_archived=False).order_by("-created_at")

        return JsonResponse(
            {
                "comments": [
                    {
                        "id": c.id,
                        "content": c.content,
                        "author": c.author.username,
                        "created_at": c.created_at,
                    }
                    for c in comments
                ]
            }
        )

    def post(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

        try:
            data = json.loads(request.body)
            content = data.get("content", "").strip()
            if not content:
                return JsonResponse({"error": "Content is required"}, status=400)

            comment = Comment.objects.create(task=task, author=request.user, content=content)
            TaskHistory.objects.create(
                task=task,
                user=request.user,
                action="Added comment",
                new_value=content,
            )
            return JsonResponse(
                {
                    "id": comment.id,
                    "content": comment.content,
                    "author": comment.author.username,
                    "created_at": comment.created_at,
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


class TaskHistoryView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

        history = task.history.filter(is_archived=False).order_by("-timestamp")
        return JsonResponse(
            {
                "history": [
                    {
                        "timestamp": h.timestamp,
                        "user": h.user.username if h.user else None,
                        "action": h.action,
                        "old_value": h.old_value,
                        "new_value": h.new_value,
                    }
                    for h in history
                ]
            }
        )
