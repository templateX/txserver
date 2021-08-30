from django.contrib import admin
from .models import Template, TemplateTag, Repo, Like


class TemplateTagInline(admin.StackedInline):
    model = TemplateTag
    extra = 0


class RepoInline(admin.StackedInline):
    model = Repo
    extra = 0


class LikeInline(admin.StackedInline):
    model = Like
    extra = 1


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TemplateTagInline, RepoInline, LikeInline]


@admin.register(TemplateTag)
class TemplateTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'tag')


@admin.register(Repo)
class RepoAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'url')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template')
