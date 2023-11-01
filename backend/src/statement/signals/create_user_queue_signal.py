from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.statement.models import Queue

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_queue(sender, instance, created, **kwargs):
    if created:
        Queue.objects.create(user=instance)
