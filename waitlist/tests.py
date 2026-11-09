from django.test import TestCase
from django.urls import reverse

from .models import Signup


def payload(**kw):
    data = {
        "name": "Ada", "business_name": "Ada's Store", "email": "ada@example.com",
        "whatsapp": "08000000000", "business_type": "fashion", "country": "Nigeria",
        "platforms": ["whatsapp", "instagram"], "monthly_messages": "20-100", "willing_to_pay": "on",
    }
    data.update(kw)
    return data


class WaitlistTests(TestCase):
    def test_home_page_loads(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Closa")

    def test_signup_creates_record_and_redirects(self):
        r = self.client.post("/", payload())
        s = Signup.objects.get()
        self.assertRedirects(r, reverse("waitlist:thanks", args=[s.referral_code]))
        self.assertEqual(s.platforms, "whatsapp,instagram")
        self.assertTrue(s.willing_to_pay)
        self.assertEqual(s.position, 1)

    def test_duplicate_email_goes_to_existing_page(self):
        self.client.post("/", payload())
        r = self.client.post("/", payload(name="Other"))
        self.assertEqual(Signup.objects.count(), 1)
        self.assertEqual(r.status_code, 302)

    def test_referral_links_and_boosts_position(self):
        for n in range(8):
            self.client.post("/", payload(email=f"u{n}@example.com"))
        late = Signup.objects.last()
        self.assertEqual(late.position, 8)
        self.client.get(f"/?ref={late.referral_code}")
        self.client.post("/", payload(email="friend@example.com"))
        friend = Signup.objects.get(email="friend@example.com")
        self.assertEqual(friend.referred_by, late)
        self.assertEqual(late.position, 3)  # 8 - 5

    def test_honeypot_blocks_bots(self):
        self.client.post("/", payload(website="spam"))
        self.assertEqual(Signup.objects.count(), 0)

    def test_thanks_page(self):
        self.client.post("/", payload())
        s = Signup.objects.get()
        r = self.client.get(reverse("waitlist:thanks", args=[s.referral_code]))
        self.assertContains(r, "#1")
        self.assertContains(r, f"ref={s.referral_code}")
