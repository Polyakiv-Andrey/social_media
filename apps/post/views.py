from rest_framework import viewsets, generics, status
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated

from apps.post.models import Post, PostLike, PostDislike
from apps.post.serializers import (
    PostCreateUpdateDeleteSerializer,
    PostListRetrieveSerializer,
    PostLikeDislikeSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return PostCreateUpdateDeleteSerializer
        return PostListRetrieveSerializer


class LikeAPIView(generics.CreateAPIView):
    queryset = PostLike.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeDislikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        like = PostLike.objects.filter(
            post_id=serializer.validated_data["post_id"],
            user_id=self.request.user.id
        )
        dislike = PostDislike.objects.filter(
            post_id=serializer.validated_data["post_id"],
            user_id=self.request.user.id
        )
        if like.exists():
            like.delete()
            return Response({"message": "Like deleted"}, status=status.HTTP_200_OK)
        if dislike.exists():
            dislike.delete()
        new_like = PostLike.objects.create(
            post_id=serializer.validated_data["post_id"],
            user_id=self.request.user.id
        )
        return Response({"message": "Liked"}, status=status.HTTP_200_OK)


class DisLikeAPIView(generics.CreateAPIView):
    queryset = PostDislike.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeDislikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        dislike = PostDislike.objects.filter(
            user_id=self.request.user.id,
            post_id=serializer.validated_data["post_id"],
        )
        like = PostLike.objects.filter(
            post_id=serializer.validated_data["post_id"],
            user_id=self.request.user.id
        )
        if dislike.exists():
            dislike.delete()
            return Response({"message": "Dislike deleted"}, status=status.HTTP_200_OK)
        if like.exists():
            like.delete()
        new_dislike = PostDislike.objects.create(
            post_id=serializer.validated_data["post_id"],
            user_id=self.request.user.id
        )
        return Response({"message": "Disliked"}, status=status.HTTP_200_OK)