import logging
import time
from django.utils.deprecation import MiddlewareMixin


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


class RequestFilter(logging.Filter):
    """Preenche campos padrão quando não vierem via extra."""
    def filter(self, record):
        for attr in [
            'path', 'method', 'user_id', 'client_ip',
            'status_code', 'response_time', 'correlation_id'
        ]:
            if not hasattr(record, attr):
                setattr(record, attr, None)
        return True


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            response_time = time.time() - request.start_time
            app_logger = logging.getLogger('django.request')
            ndjson_logger = logging.getLogger('requests')
            payload = {
                'status_code': response.status_code,
                'response_time': round(response_time, 4),
                'path': getattr(request, 'path', None),
                'method': getattr(request, 'method', None),
                'user_id': getattr(getattr(request, 'user', None), 'id', None) if getattr(request, 'user', None) and request.user.is_authenticated else None,
                'client_ip': _get_client_ip(request),
                'correlation_id': getattr(request, 'correlation_id', None),
            }
            app_logger.info('request', extra=payload)
            ndjson_logger.info('request', extra=payload)
        return response
