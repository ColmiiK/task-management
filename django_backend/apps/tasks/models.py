from django.db import models
from apps.users.models import User
from apps.common.models import Tag

STATUS_CHOICES = [("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")]
PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES)
    priority = models.CharField(choices=PRIORITY_CHOICES)
    due_date = models.DateTimeField()
    estimated_hours = models.DecimalField(decimal_places=2, max_digits=2)
    actual_hours = models.DecimalField(null=True, decimal_places=2, max_digits=2)

    # Relationships
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_created"
    )
    assigned_to = models.ManyToManyField(User, related_name="task_assigned")
    tags = models.ManyToManyField(Tag)
    parent_task = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

    # Metadata
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)


class TaskAssigment(models.Model):
    pass


class TaskHistory(models.Model):
    pass


class TaskTemplate(models.Model):
    pass
