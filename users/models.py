from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import hashlib


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('customer', _('Customer')),
        ('vendor', _('Vendor')),
    )

    email = models.EmailField(_('email address'), unique=True, db_index=True)
    full_name = models.CharField(_('full name'), max_length=100, db_index=True)
    user_type = models.CharField(_('user type'), max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    image = models.ImageField(_('profile image'), upload_to='user_images/', null=True, blank=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    vendor_profile = models.OneToOneField('vendors.Vendor', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile')
    is_verified_vendor = models.BooleanField(_('verified vendor'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        creating = self.pk is None
        if self.image:
            self.image.name = self.generate_image_filename(self.image.name)
        super().save(*args, **kwargs)

        # Automatically create Vendor if user_type is 'vendor'
        if self.user_type == 'vendor' and creating:
            from vendors.models import Vendor  # Avoid circular import
            if not hasattr(self, 'vendor'):
                store_name = f"{self.full_name}'s Store"
                Vendor.objects.create(
                    user=self,
                    store_name=store_name[:100]  # truncate to avoid DB error
                )


    def generate_image_filename(self, filename):
        ext = filename.split('.')[-1]
        hashed_email = hashlib.sha256(self.email.encode('utf-8')).hexdigest()
        filename = f'{hashed_email}.{ext}'
        return f'user_{hashed_email}/{filename}'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [
            models.Index(fields=['full_name']),
        ]