from django import forms

from .models import Signup

PLATFORM_CHOICES = [
    ("whatsapp", "WhatsApp"),
    ("instagram", "Instagram"),
    ("tiktok", "TikTok"),
    ("facebook", "Facebook"),
    ("website", "Website"),
    ("email", "Email"),
]

VOLUME_CHOICES = [
    ("", "Choose one"),
    ("0-20", "0–20"),
    ("20-100", "20–100"),
    ("100-500", "100–500"),
    ("500+", "500+"),
]


class SignupForm(forms.ModelForm):
    platforms = forms.MultipleChoiceField(
        choices=PLATFORM_CHOICES, widget=forms.CheckboxSelectMultiple, required=False
    )
    monthly_messages = forms.ChoiceField(choices=VOLUME_CHOICES, required=False)
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # honeypot

    class Meta:
        model = Signup
        fields = [
            "name", "business_name", "email", "whatsapp", "business_type",
            "country", "platforms", "monthly_messages", "willing_to_pay",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "business_name": forms.TextInput(),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "whatsapp": forms.TextInput(attrs={"autocomplete": "tel"}),
            "country": forms.TextInput(attrs={"autocomplete": "country-name"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["business_type"].choices = [("", "Choose one")] + list(Signup.BUSINESS_TYPES)

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""

    def clean_platforms(self):
        return ",".join(self.cleaned_data.get("platforms") or [])
