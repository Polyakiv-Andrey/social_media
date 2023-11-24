from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user

        if user.is_authenticated:
            user.time_last_action = timezone.now()
            user.save()

        return response
