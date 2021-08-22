import uuid
from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#specifying-a-custom-user-model
    """
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    cipher = models.CharField(_('cipher'), max_length=44, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Card(models.Model):

    # Длинна поля 1368 символов рассчитывалась следующим образом:
    # исходные данные: максимальная длинна пользовательских данных = 254 символа в utf-8, хранение в base64
    # 1. переводим utf-8 (максимум 4 байта на символ) в байты: 254 симивола * 4 байта = 1016 байт
    # 2. проверяем кратно ли блоку AES (16 байт): 1016 / 16 = 63.5 -> 64 блока * 16 байт = 1024 байта
    # 3. переводим в base64 (каждые 3 исходных байта кодируются 4 символами): 1024 / 3 * 4 = 1366 символа
    # 4. base64 строка должна быть кратна 4: 1366 / 4 = 341.5 -> 342 * 4 = 1368 символов

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(_('username'), max_length=1368)
    password = models.CharField(_('password'), max_length=1368)
    notes = models.CharField(_('notes'), max_length=2668, blank=True)
    is_favorite = models.BooleanField(_('favorite'), blank=True, default=False)
    is_deleted = models.BooleanField(_('deleted'), default=False)

    @classmethod
    def mark_as_deleted(cls, owner, id):
        query = cls.objects.filter(owner=owner, id=id, is_deleted=False)

        if query.count() == 0:
            return False

        query.update(is_deleted=True)
        return True


class AuditCard(models.Model):
    ACTIONS_LIST = [
        ('c', 'created'),
        ('m', 'modified'),
        ('d', 'deleted'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=1, choices=ACTIONS_LIST)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class SiteCard(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    uri = models.CharField(_('uri'), max_length=1368)
    host = models.CharField(_('host'), max_length=1368)

    @classmethod
    def check_unique(cls, owner, username, uri):
        query = cls.objects.filter(card__owner=owner, card__username=username, uri=uri, card__is_deleted=False)
        return False if query.exists() else True
