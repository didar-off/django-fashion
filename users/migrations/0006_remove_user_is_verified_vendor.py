# Generated by Django 4.2 on 2025-04-09 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_verified_vendor',
        ),
    ]
