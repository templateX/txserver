from django.contrib import admin
from .models import Template, Template_Tag, Repo, Like

class TemplateTagInline(admin.StackedInline):
    model = Template_Tag
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

@admin.register(Template_Tag)
class TemplateTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'tag')

@admin.register(Repo)
class RepoAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'link')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template')
