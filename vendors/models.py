from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import hashlib


class Vendor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='vendor')
    store_name = models.CharField(_('store name'), max_length=100, db_index=True)
    store_logo = models.ImageField(_('store logo'), upload_to='store_logos/', null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    is_verified = models.BooleanField(_('verified'), default=False)

    def __str__(self):
        return self.store_name

    def save(self, *args, **kwargs):
        if self.store_logo:
            self.store_logo.name = self.generate_logo_filename(self.store_logo.name)
        super().save(*args, **kwargs)

    def generate_logo_filename(self, filename):
        ext = filename.split('.')[-1]
        hashed_store_name = hashlib.sha256(self.store_name.encode('utf-8')).hexdigest()
        filename = f'{hashed_store_name}.{ext}'
        return f'vendor_{hashed_store_name}/{filename}'

    class Meta:
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')
        indexes = [
            models.Index(fields=['store_name']),
        ]