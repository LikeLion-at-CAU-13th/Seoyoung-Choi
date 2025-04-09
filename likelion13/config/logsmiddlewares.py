import logging
from django.utils.timezone import now

logger = logging.getLogger('django.request')  # 설정한 로거 이름과 동일해야 함

class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 로그 남기기: 시간, 메서드, URL
        logger.info(f"{now()} | {request.method} {request.get_full_path()}")

        response = self.get_response(request)
        return response
