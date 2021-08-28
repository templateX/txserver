from django.db import models
from django.utils.text import slugify
from django.conf import settings
from tags.models import Tag


class Template(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='templates')
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    preview_link = models.URLField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True, through='Template_Tag', through_fields=('template', 'tag'))
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through='Like', through_fields=('template', 'user'))

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'templates'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Template, self).save(*args, **kwargs)

    @property
    def like_count(self):
        return self.likes.count()


class Template_Tag(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'template_tags'
        unique_together = ('template', 'tag')

    def __str__(self) -> str:
        return self.tag.name + ' used in ' + self.template.title


class Repo(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='repos')
    provider = models.CharField(max_length=10, blank=True, null=True)
    link = models.URLField()

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        db_table = 'repos'


class Like(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='template_liked')

    class Meta:
        db_table = 'likes'
        unique_together = ('user', 'template')

    def __str__(self) -> str:
        return str(self.id)
