from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import RegistrationOTC
from apps.authentication.serializers import (
    RegistrationSerializer,
    ValidateCodeSerializer,
    CreateUserSerializer,
    LoginSerializer
)

User = get_user_model()


class RegistrationSendOTCCodeAPIView(generics.CreateAPIView):
    queryset = RegistrationOTC.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    authentication_classes = ()


class RegistrationValidateOTCCodeAPIView(generics.CreateAPIView):
    queryset = RegistrationOTC.objects.all()
    serializer_class = ValidateCodeSerializer
    permission_classes = [AllowAny]
    authentication_classes = ()


class RegistrationCreateUserCodeAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]
    authentication_classes = ()


class UserLoginApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email__iexact=request.data.get('email').lower()).first()

        if not user or not user.check_password(request.data.get('password')):
            return Response(
                {'detail': "No active account found with the given credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }
        )
