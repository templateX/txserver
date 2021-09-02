from django.core.exceptions import ObjectDoesNotExist
from templates.models import Template, Like
from tags.models import Tag
from .exceptions import TemplateUnavailable, TagUnavailable
from api.v1.response import InvalidPermission


class TemplateAuthLookUpMixin:
    def get_template(self):
        id = self.kwargs['template_id']
        try:
            obj = Template.objects.get(id=id)

            # Template User Permissions
            if not self.request.user == obj.user:
                raise InvalidPermission

            return obj
        except Template.DoesNotExist:
            raise TemplateUnavailable


class TemplateLookUpMixin:
    def get_template(self):
        id = self.kwargs['template_id']
        try:
            obj = Template.objects.get(id=id)
            return obj
        except Template.DoesNotExist:
            raise TemplateUnavailable


class TagLookUpMixin:
    def get_tag(self):
        id = self.kwargs['tag_id']
        try:
            obj = Tag.objects.get(id=id)
            return obj
        except Tag.DoesNotExist:
            raise TagUnavailable


class LikeLookupMixix:
    def get_like(self, user, template):
        try:
            obj = Like.objects.get(template=template, user=user)
            return obj
        except Like.DoesNotExist:
            return None
