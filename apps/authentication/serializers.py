import random
import string
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model, login
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import RegistrationOTC
from social_network import settings
from .tasks import send_email_task
User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationOTC
        fields = ["email"]

    def validate_email(self, email):
        user = User.objects.filter(email=email.lower())
        if user.exists():
            raise serializers.ValidationError("User with this email exist!")
        return email

    def create(self, validated_data):
        RegistrationOTC.objects.filter(email=validated_data["email"].lower()).delete()
        otc = RegistrationOTC.objects.create(
            email=validated_data["email"].lower(),
            code=''.join(random.choices(string.digits, k=6))
        )
        data_dict = {"subject": 'Social Media Registration Confirmation', "code": otc.code}
        send_email_task.delay(settings.REGISTRATION_CONFIRMATION_TEMPLATE_ID, data_dict, otc.email.lower())
        return validated_data


class ValidateCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        otc = RegistrationOTC.objects.filter(email=attrs["email"], code=attrs["code"]).first()

        if otc and (timezone.localtime(timezone.now()) - otc.created) < timedelta(minutes=15) and not otc.is_used:
            return attrs
        raise serializers.ValidationError("Code does not exist or has expired!")

    def create(self, validated_data):
        otc = RegistrationOTC.objects.filter(email=validated_data["email"].lower(), code=validated_data["code"]).first()
        otc.is_used = True
        otc.confirmed = True
        otc.save()
        return validated_data


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)
    access_token = serializers.CharField(read_only=True, )
    refresh_token = serializers.CharField(read_only=True, )

    class Meta:
        model = User
        fields = ["email", "password", "password_confirmation", "access_token", "refresh_token"]

    def validate_email(self, email):
        user = User.objects.filter(email=email.lower())
        if user.exists():
            raise serializers.ValidationError("User with this email exist!")
        otc = RegistrationOTC.objects.filter(email=email.lower()).first()
        if otc and otc.confirmed is True:
            return email
        raise serializers.ValidationError("Email not confirmed!")

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_password_confirmation(self, password_confirmation):
        if password_confirmation != self.initial_data.get('password'):
            raise serializers.ValidationError("Passwords do not match")
        return password_confirmation

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data["email"], password=validated_data["password"])
        login(self.context["request"], user)
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True, write_only=True)
    password = serializers.CharField(max_length=100, required=True, write_only=True)