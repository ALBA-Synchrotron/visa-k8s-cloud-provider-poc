# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import exception_handler

from settings import labels
from mis_template.utils.request import JSONResponse


class DryRunException(Exception):
    pass


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and 'status_code' in response.data:
        response.data['status_code'] = response.status_code

    if response and response.data:
        if str(response.data) == str(exc):
            error_message = response.data
            if type(error_message) == list and len(error_message) == 1:
                error_message = error_message[0]
            return JSONResponse({'error': error_message}, status=response.status_code)
        else:
            return JSONResponse({'error': str(exc)}, status=response.status_code)

    status_code = status.HTTP_400_BAD_REQUEST

    if issubclass(exc.__class__, ObjectDoesNotExist):
        status_code = status.HTTP_404_NOT_FOUND

    if exc and hasattr(exc, 'message') and exc.message:
        return JSONResponse({'error': exc.message}, status=status_code)

    if exc and hasattr(exc, 'messages') and exc.messages and len(exc.messages) == 1:
        return JSONResponse({'error': exc.messages[0]}, status=status_code)
    if exc:
        return JSONResponse({'error': str(exc)}, status=status_code)
    return JSONResponse({'error': labels.UNKNOWN_ERROR}, status=status_code)
