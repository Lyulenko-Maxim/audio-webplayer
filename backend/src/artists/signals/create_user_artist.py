from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.artists.models import Artist

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_artist(sender, instance, created, **kwargs):
    if instance.is_artist:
        Artist.objects.get_or_create(user=instance, defaults={'user': instance})
