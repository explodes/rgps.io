import random
import re

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rgps.app import managers


class User(AbstractBaseUser, PermissionsMixin):
    """
    A custom user class that basically mirrors Django's `AbstractUser` class
    and doesn't force `first_name` or `last_name` with sensibilities for
    international names.

    http://www.w3.org/International/questions/qa-personal-names
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters and numbers.'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[A-Za-z0-9]+$'),
                                                              _('Enter a valid username.'),
                                                              'invalid')
                                ])
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    email = models.EmailField(max_length=512, null=True)

    registration_id = models.CharField(max_length=2048, null=True)
    google_oauth2 = models.CharField(max_length=2048, null=True)

    token = models.CharField(max_length=128, null=True, unique=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    altitude = models.FloatField(null=True)

    objects = managers.UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username


    def get_full_name(self):
        return self.get_username()

    def get_short_name(self):
        return self.get_username()

    @staticmethod
    def generate_token():
        while True:
            token = '%x' % random.getrandbits(128 * 4)
            if not User.objects.filter(token=token).exists():
                return token



