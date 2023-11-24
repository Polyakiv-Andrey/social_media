from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.post.views import PostViewSet

router = SimpleRouter()

router.register(r'', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),

]

app_name = "post"
