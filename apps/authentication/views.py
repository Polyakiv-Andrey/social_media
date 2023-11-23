from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.authentication.models import RegistrationOTC
from apps.authentication.serializers import (
    RegistrationSerializer,
    ValidateCodeSerializer,
    CreateUserSerializer
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