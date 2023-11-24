from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


from apps.authentication.manager import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField()
    image = models.ImageField(upload_to="photo/", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    time_last_action = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def clean(self):
        if User.objects.filter(email=self.email).exists():
            raise ValidationError(detail={'email': ["Email exists"]})

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class RegistrationOTC(models.Model):
    code = models.CharField()
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email}, {self.code}"
