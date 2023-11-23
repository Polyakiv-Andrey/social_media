from django.urls import path, include

urlpatterns = [
    path("auth/", include("apps.authentication.urls", namespace="auth")),
]

app_name = "api"
