from django.db.models import signals
from django.dispatch import receiver

from . import models

# TODO: ezek még nincsenek kipróbálva, tesztelve


@receiver(signals.post_save, sender=models.AssetRequest)
def on_asset_request_save(sender, instance, created, **kwargs):
    icon = instance.type.icon()
    if icon is None:
        icon = 'create' if created else 'update'
    models.FeedItem.objects.create(
        name=instance.name,
        icon=icon,
        asset_request=instance,
        aid_center=instance.aid_center,
        status_old=None if created else instance.status,
        status_new=instance.status,
    )


@receiver(signals.post_delete, sender=models.AssetRequest)
def on_asset_request_delete(sender, instance, **kwargs):
    icon = instance.type.icon() if instance.type is not None else None
    if icon is None:
        icon = 'delete'
    models.FeedItem.objects.create(
        name=instance.name,
        icon=icon,
        asset_request=instance,
        aid_center=instance.aid_center,
        status_old=instance.status,
    )
