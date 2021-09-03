import uuid
from django.db import models
from templates.models import Template
from django.conf import settings


class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookmarks'
        ordering = ('-created_at',)
        unique_together = ('template', 'user')

    def __str__(self) -> str:
        return str(self.id)
