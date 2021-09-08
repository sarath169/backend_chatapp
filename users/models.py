"""
Models related to User
"""
from django.core import validators
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.validators import validate_password


class UserManager(BaseUserManager):
    """
    """
    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        user = self.create_user(password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model to store user details like their first name, last name, email, etc.
    Email field is unique for each user.
    """
    first_name = models.CharField(
        _('first name'), max_length=150, blank=True,
        help_text=_('First name of the User.'),
    )
    last_name = models.CharField(
        _('last name'), max_length=150, blank=True,
        help_text=_('Last name of the User.')
    )
    email = models.EmailField(
        _('email address'), max_length=255, unique=True,
        help_text=_('Email address of the user.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Please enter valid email. Only letters, numbers, ' ' and '
                    '@/./+/-/_ characters allowed.')
            )
        ]
    )
    password = models.CharField(
        _('password'), max_length=128, validators=[validate_password],
        null=True, blank=True
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return "{id} - {email}".format(id=self.id, email=self.email)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name


class UserSocialAccount(models.Model):
    """
    To store the social accounts used by a user.
    """
    GOOGLE, FACEBOOK, GITHUB = 'google', 'facebook', 'github'
    ACCOUNT_CHOICES = (
        (GOOGLE, "Google"),
        (FACEBOOK, "Facebook"),
        (GITHUB, "Github"),
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="social_accounts"
    )
    account_type = models.CharField(choices=ACCOUNT_CHOICES, max_length=64)
    account_id = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_social_account'
        verbose_name = _('user_social_account')
        verbose_name_plural = _('user_social_accounts')

    def __str__(self):
        return "{id} - {email}: {account_type}".format(
            id=self.id, email=self.user, account_type=self.account_type)
