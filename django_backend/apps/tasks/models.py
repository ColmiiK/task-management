from django.db import models
from users.models import User


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES)
    priority = models.CharField(choices=PRIORITY_CHOICES)
    due_date = models.DateTimeField()
    estimated_hours = models.DecimalField()
    actual_hours = models.DecimalField(null=True)

    # Relationships
    created_by = models.ForeignKey(User)
    assigned_to = models.ManyToManyField(User)
    tags = models.ManyToManyField(Tag)
    parent_task = models.ForeignKey("self", null=True)

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
