from rest_framework.exceptions import APIException

class ExistingAccount(APIException):
    status_code = 403
    default_detail = 'Account already exists'

class InvalidCredentials(APIException):
    status_code = 401
    default_detail = 'Either username or password is incorrect'
