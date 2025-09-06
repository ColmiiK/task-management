from django.db import models
from apps.users.models import User
from apps.common.models import Tag
from apps.common.managers import SoftDeleteModel

STATUS_CHOICES = [("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")]
PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]


class Task(SoftDeleteModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES)
    priority = models.CharField(choices=PRIORITY_CHOICES)
    due_date = models.DateTimeField()
    estimated_hours = models.DecimalField(decimal_places=2, max_digits=5)
    actual_hours = models.DecimalField(null=True, decimal_places=2, max_digits=5)

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

    def __str__(self):
        return f"{self.title} - {self.status}"


class TaskAssigment(SoftDeleteModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assigned_tasks_by"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assigned_by} assigned to {self.task}"


class TaskHistory(SoftDeleteModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ({self.action}) on {self.task}"


class TaskTemplate(SoftDeleteModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    default_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    default_priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    default_estimated_hours = models.DecimalField(
        max_digits=5, decimal_places=2, default=1.0
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="task_templates"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
