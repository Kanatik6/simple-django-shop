from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.products.models import Cart


User = get_user_model()

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    print("началось")
    if kwargs.get('created'):
        print('создается')
        Cart.objects.create(user=instance)
        print('создалось')
