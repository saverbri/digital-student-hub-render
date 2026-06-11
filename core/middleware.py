from .models import AuditLog

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Записываем действия авторизованных пользователей, исключая статику и медиа
        if request.user.is_authenticated and not request.path.startswith('/static') and not request.path.startswith('/media'):
            # Записываем POST-запросы, а также GET-запросы к админке (можно изменить)
            if request.method in ['POST', 'PUT', 'DELETE'] or (request.method == 'GET' and 'admin' in request.path):
                action = f"{request.method} {request.path}"
                AuditLog.objects.create(
                    user=request.user,
                    action=action,
                    ip_address=self.get_client_ip(request),
                    details={
                        'method': request.method,
                        'path': request.path,
                        'data': dict(request.POST) if request.method == 'POST' else None,
                    }
                )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip