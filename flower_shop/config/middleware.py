from django.urls import reverse
from django.shortcuts import redirect
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class ClearCacheMiddleware(MiddlewareMixin):
    def process_request(self, request):
        response = self.get_response(request)

        # Если пользователь вошел или вышел
        if request.path == reverse('account_login') or request.path == reverse('account_logout'):
            # Очищаем кэш
            cache.clear()

        return response


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        public_urls = [
            reverse('account_login'),
            reverse('account_signup'),
            reverse('account_logout'),
        ]

        if not request.user.is_authenticated and request.path not in public_urls:
            return redirect('account_login')

        response = self.get_response(request)
        return response
