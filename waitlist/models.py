import secrets

from django.conf import settings
from django.db import models


def make_code():
    return secrets.token_urlsafe(6).replace("-", "").replace("_", "")[:8].upper()


class Signup(models.Model):
    BUSINESS_TYPES = [
        ("fashion", "Fashion & beauty"),
        ("food", "Food & restaurants"),
        ("ecommerce", "E-commerce / online store"),
        ("real_estate", "Real estate"),
        ("health", "Clinic / health & wellness"),
        ("education", "School / education / courses"),
        ("services", "Services (salon, cleaning, repairs…)"),
        ("agency", "Agency / freelancer"),
        ("events", "Events & hospitality"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=120)
    business_name = models.CharField(max_length=160)
    email = models.EmailField(unique=True)
    whatsapp = models.CharField("WhatsApp number", max_length=30, blank=True)
    business_type = models.CharField(max_length=30, choices=BUSINESS_TYPES)
    country = models.CharField(max_length=60)
    platforms = models.CharField(max_length=200, blank=True, help_text="Comma-separated channels they sell on")
    monthly_messages = models.CharField(max_length=30, blank=True)
    willing_to_pay = models.BooleanField(default=False, help_text="Ticked 'reserve my early-access price'")

    referral_code = models.CharField(max_length=12, unique=True, default=make_code, editable=False)
    referred_by = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="referrals"
    )

    source = models.CharField(max_length=60, blank=True, help_text="utm_source or ?ref channel")
    contacted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.business_name} ({self.email})"

    @property
    def referral_count(self):
        return self.referrals.count()

    @property
    def position(self):
        """Signup order, moved up REFERRAL_BOOST places for each referral."""
        base = Signup.objects.filter(created_at__lt=self.created_at).count() + 1
        return max(1, base - self.referral_count * settings.REFERRAL_BOOST)

    @property
    def in_early_access(self):
        return self.position <= settings.EARLY_ACCESS_SPOTS
