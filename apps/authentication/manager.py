from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create(self, email, password=None):
        if not email:
            raise ValueError(['Please provide an email address'])
        if not password:
            raise ValueError(['Please provide a password'])

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None):
        return self.create(email, password)

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError(['Please provide an email address'])
        if not password:
            raise ValueError(['Please provide a password'])

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
