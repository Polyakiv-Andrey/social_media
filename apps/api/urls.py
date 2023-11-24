from django.urls import path, include

urlpatterns = [
    path("auth/", include("apps.authentication.urls", namespace="auth")),
    path("post/", include("apps.post.urls", namespace="post")),
    path("analytics/", include("apps.analytics.urls", namespace="analytics")),
]

app_name = "api"
