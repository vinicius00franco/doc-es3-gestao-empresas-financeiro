import uuid
from django.utils.deprecation import MiddlewareMixin


class CorrelationIdMiddleware(MiddlewareMixin):
    HEADER_NAME = 'HTTP_X_CORRELATION_ID'
    RESPONSE_HEADER = 'X-Correlation-ID'

    def process_request(self, request):
        cid = request.META.get(self.HEADER_NAME)
        if not cid:
            cid = uuid.uuid4().hex
        request.correlation_id = cid

    def process_response(self, request, response):
        cid = getattr(request, 'correlation_id', None)
        if cid:
            response[self.RESPONSE_HEADER] = cid
        return response