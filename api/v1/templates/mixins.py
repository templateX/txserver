from templates.models import Template
from .exceptions import TemplateUnavailable
from api.v1.response import InvalidPermission


class TemplateLookUpMixin:
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
