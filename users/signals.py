from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VerificationCode, User
import random
import string


def generate_verification_code(length=6):
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(length)).upper()


@receiver(post_save, sender=User)
def create_verification_code(sender, instance, created, **kwargs):
    if created:
        code = generate_verification_code()  # generate a random code
        VerificationCode.objects.create(user=instance, code=code)
