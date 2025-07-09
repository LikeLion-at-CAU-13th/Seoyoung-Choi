from django.http import JsonResponse
from django.http import Http404
from django.core.exceptions import PermissionDenied
from config.custom_exceptions import *

class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        error_info = self._get_error_info(exception)

        response_data = self._create_unified_response(request, error_info)

        return JsonResponse(
            response_data,
            status=error_info['status_code'] if 'status_code' in error_info else 500,
        )
    
    def _get_error_info(self, exception):
        #if isinstance(exception, Http404):
            #return {
                #'message': 'Resource not found.',
                #'status_code': 404,
                #'code': 'NOT-FOUND'
            #}
        if isinstance(exception, BaseCustomException):
            return {
                'message': exception.detail,
                'status_code': exception.status_code,
                'code': exception.code
            }
        elif isinstance(exception, ResourceNotFoundException):
            return {
                'message': exception.detail,
                'status_code': exception.status_code,
                'code': exception.code
            }
        elif isinstance(exception, PermissionDenied):
            return {
                'message': 'Permission denied.',
                'status_code': 403,
                'code': 'PERMISSION-DENIED'
            }
        else:
            return {
                'message': 'Internal server error.',
                'status_code': 500,
                'code': 'INTERNAL-ERROR'
            }
        
    def _create_unified_response(self, request, error_info):
        return {
            'success': False,
            'error': {
                'code': error_info.get('code', 'UNKNOWN_ERROR'),
                'message': error_info.get('message', 'An error occurred.'),
                'status_code': error_info.get('status_code', 500),
            }
        }
   