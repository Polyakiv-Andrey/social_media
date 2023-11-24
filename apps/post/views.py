from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.post.models import Post
from apps.post.serializers import PostCreateUpdateDeleteSerializer, PostListRetrieveSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return PostCreateUpdateDeleteSerializer
        return PostListRetrieveSerializer
