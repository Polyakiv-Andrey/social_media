from django.urls import path

from apps.authentication.views import (
    RegistrationSendOTCCodeAPIView,
    RegistrationValidateOTCCodeAPIView,
    RegistrationCreateUserCodeAPIView, UserLoginApiView,
)

urlpatterns = [
    path("registration-send-code/", RegistrationSendOTCCodeAPIView.as_view(), name="registration-send-code"),
    path(
        "registration-validate-code/",
        RegistrationValidateOTCCodeAPIView.as_view(),
        name="registration-validate-code"
    ),
    path("registration-create-user/", RegistrationCreateUserCodeAPIView.as_view(), name="registration-send-code"),
    path("login/", UserLoginApiView.as_view(), name="login")

]

app_name = "auth"
