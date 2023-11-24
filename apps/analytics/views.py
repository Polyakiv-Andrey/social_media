from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.analytics.serializers import UserActivitySerializer
from apps.post.models import PostLike
User = get_user_model()


class LikeAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'date_from',
                openapi.IN_QUERY,
                description="Amount likes from date (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'date_to',
                openapi.IN_QUERY,
                description="Amount likes to date (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        likes = PostLike.objects.all()
        if date_from:
            likes = likes.filter(date_created__gte=date_from)
        if date_to:
            likes = likes.filter(date_created__lte=date_to)
        return Response({"like_amount": likes.count()}, status=status.HTTP_200_OK)


class UserActivityAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
