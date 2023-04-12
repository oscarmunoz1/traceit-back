from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from .managers import UserManager
from .constants import USER_TYPE_CHOICES, CONSUMER
from company.models import Company, Establishment
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None  # remove username field, we will use email as unique identifier
    email = models.EmailField(unique=True, null=True, db_index=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    companies = models.ManyToManyField(
        Company,
        related_name="company_users",
        through="WorksIn",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=CONSUMER
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = UserManager()


class WorksIn(models.Model):
    USER_ROLES = [
        ("CA", _("Company Admin")),
        ("DS", _("Domain Supervisor")),
        ("DW", _("Domain Worker")),
        ("DE", _("Dealer")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_workers"
    )
    role = models.CharField(choices=USER_ROLES, max_length=5)
    establishments_in_charge = models.ManyToManyField(
        Establishment, related_name="workers", blank=True, null=True
    )
    role_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True
    )


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "code")

    def __str__(self):
        return f"{self.user.email} - {self.code}"
