import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from tags.models import Tag


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='templates')
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True, unique=True)
    description = models.TextField()
    preview_link = models.URLField(blank=True, null=True)

    # tags = models.ManyToManyField(Tag, blank=True, through='Template_Tag', through_fields=('template', 'tag'))
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through='Like', through_fields=('template', 'user'))

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'templates'
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Template, self).save(*args, **kwargs)

    @property
    def like_count(self):
        return self.likes.count()


class TemplateTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='template_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_templates')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'template_tags'
        unique_together = ('template', 'tag')

    def __str__(self) -> str:
        return self.tag.name + ' used in ' + self.template.title


class Repo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='repos')
    provider = models.CharField(max_length=10, blank=True, null=True)
    url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        db_table = 'repos'


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='template_likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_likes')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
        unique_together = ('user', 'template')

    def __str__(self) -> str:
        return str(self.id)
