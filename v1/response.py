from rest_framework.exceptions import APIException


class Success(APIException):
    status_code = 200
    default_detail = 'SUCCESS'


class SuccessCreate(APIException):
    status_code = 201
    default_detail = 'SUCCESSFULLY CREATED'


class SuccessDelete(APIException):
    status_code = 204
    default_detail = 'SUCCESSFULLY DELETED'


class SuccessUpdate(APIException):
    status_code = 204
    default_detail = 'SUCCESSFULLY UPDATED'


class InvalidPermission(APIException):
    status_code = 403
    default_detail = 'You do not have permission to perform this action.'
