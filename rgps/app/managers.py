from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username,
                          is_staff=False, is_active=True, is_superuser=False,
                          **extra_fields)
        user.set_password(password)
        user.token = self.model.generate_token()
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password=password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user


class TokenManager(Manager):
    pass
