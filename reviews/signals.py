from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review


@receiver(post_save, sender=Review)
def update_average_rating(sender, instance, **kwargs):
    production = instance.production
    production.update_reputation()
