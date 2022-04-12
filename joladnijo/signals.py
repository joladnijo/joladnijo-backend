from django.db.models import signals
from django.dispatch import receiver

from . import models


@receiver(signals.post_delete, sender=models.AssetRequest)
def on_asset_request_delete(sender, instance, **kwargs):
    icon = instance.type.icon()
    if icon is None or len(icon) == 0:
        icon = 'delete'
    models.FeedItem.objects.create(
        name=instance.name,
        icon=icon,
        asset_request=instance,
        aid_center=instance.aid_center,
        status_old=instance.status,
    )


'''
@receiver(signals.post_save, sender=models.FeedItem)
def on_asset_request_save(sender, instance, created, **kwargs):
    # TODO: értesítő e-mail küldése innen?
    pass
'''
