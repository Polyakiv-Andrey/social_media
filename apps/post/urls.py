from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.post.views import PostViewSet, LikeAPIView, DisLikeAPIView

router = SimpleRouter()

router.register(r'', PostViewSet, basename='post')

urlpatterns = [
    path("like/", LikeAPIView.as_view(), name="like"),
    path("dislike/", DisLikeAPIView.as_view(), name="dislike"),
    path('', include(router.urls)),
]

app_name = "post"
