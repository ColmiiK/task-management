from django.db import models
from django.utils.timezone import now


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_archived=True, archived_at=now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_archived=False)

    def archived(self):
        return self.filter(is_archived=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def all_with_archived(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def archived(self):
        return self.all_with_archived().archived()

    def hard_delete(self):
        return self.all_with_archived().hard_delete()


class SoftDeleteModel(models.Model):
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_archived = True
        self.archived_at = now()
        self.save()
