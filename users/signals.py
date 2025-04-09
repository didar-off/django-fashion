from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from users.models import User
from vendors.models import Vendor


@receiver(post_save, sender=User)
def handle_vendor_status(sender, instance, created, **kwargs):
    def create_or_delete_vendor():
        if instance.is_vendor:
            Vendor.objects.get_or_create(
                user=instance,
                defaults={'store_name': f"{instance.full_name}'s Store"}
            )
        else:
            Vendor.objects.filter(user=instance).delete()
    transaction.on_commit(create_or_delete_vendor)