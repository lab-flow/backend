from django.db import Error

from drf_standardized_errors.handler import ExceptionHandler

from rest_framework.exceptions import APIException


class DjangoDbError(APIException):
    status_code = 400
    default_detail = "Django DB error."
    default_code = "django_db_error"


class RequestDataError(APIException):
    status_code = 400
    default_detail = "Request data error."
    default_code = "request_data_error"


class QueryParamError(APIException):
    status_code = 400
    default_detail = "Query param error."
    default_code = "query_param_error"


class DrfExceptionHandler(ExceptionHandler):
    def convert_known_exceptions(self, exc: Exception) -> Exception:
        if issubclass(type(exc), Error):
            return DjangoDbError(str(exc))

        return super().convert_known_exceptions(exc)
