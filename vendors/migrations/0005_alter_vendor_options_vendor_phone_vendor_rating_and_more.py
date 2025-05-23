# Generated by Django 4.2 on 2025-04-09 17:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendors', '0004_alter_vendor_store_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ['-is_verified', '-rating'], 'verbose_name': 'vendor', 'verbose_name_plural': 'vendors'},
        ),
        migrations.AddField(
            model_name='vendor',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='phone number'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='rating',
            field=models.FloatField(default=0.0, verbose_name='rating'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='verified_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='verification date'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='website'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='verified status'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='store_logo',
            field=models.ImageField(blank=True, null=True, upload_to='store_logos/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])], verbose_name='store logo'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='store_name',
            field=models.CharField(max_length=100, unique=True, verbose_name='store name'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddIndex(
            model_name='vendor',
            index=models.Index(fields=['rating'], name='vendors_ven_rating_1e84ed_idx'),
        ),
    ]
