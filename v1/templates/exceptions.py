from rest_framework.exceptions import APIException


class TemplateUnavailable(APIException):
    status_code = 404
    default_detail = 'Template not found'


class TagUnavailable(APIException):
    status_code = 404
    default_detail = 'Tag not found'


class RepoUnavailable(APIException):
    status_code = 404
    default_detail = 'Repo not found'


class InvalidData(APIException):
    status_code = 409
    default_detail = 'Invalid detail'
