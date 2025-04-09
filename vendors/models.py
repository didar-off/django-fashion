import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from users.models import User
from core.models import TimeStampedModel


class Vendor(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='vendor',
        verbose_name=_('user')
    )
    
    store_name = models.CharField(_('store name'), max_length=100, unique=True)
    store_logo = models.ImageField(
        _('store logo'),
        upload_to='store_logos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    description = models.TextField(_('description'), blank=True, null=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    website = models.URLField(_('website'), blank=True, null=True)
    is_verified = models.BooleanField(_('verified status'), default=False)
    verified_at = models.DateTimeField(_('verification date'), blank=True, null=True)
    rating = models.FloatField(_('rating'), default=0.0)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')

    def __str__(self):
        return self.store_name

    def save(self, *args, **kwargs):
        if self.store_logo:
            self.store_logo.name = self._generate_filename(self.store_logo.name)
        super().save(*args, **kwargs)

    def _generate_filename(self, filename):
        ext = filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{ext}"
        return f"vendor_{self.pk}/{new_filename}"