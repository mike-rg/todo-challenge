from django.http import Http404

from rest_framework.exceptions import APIException
from rest_framework.response import Response


class AssignmentApiExceptionHandler(APIException):
    def format_response(self, exc):
        if isinstance(exc, Http404):
            message = str(exc)
        else:
            message = str(exc.default_detail)
        response = {"status": self.status_code, "data": {"message": message, "results": {}}}
        return Response(response, status=self.status_code)
