# Closa — Waitlist

Landing page + early-access waitlist for Closa, the AI salesperson for WhatsApp, Instagram, TikTok, email and website chat.

## Features
- Landing page: animated chat demo, pricing (USD/NGN toggle), FAQ
- Waitlist form: business type, country, channels, message volume, "reserve founding price" (validation signal)
- Referral system: each signup gets a link; every referral moves them up 5 places
- Admin (`/admin`): filters, search, "contacted" checkbox, CSV export
- Honeypot spam protection, duplicate emails go to their existing page

## Run locally
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Deploy on Render
Push to GitHub, then New → Blueprint and pick this repo (uses `render.yaml`: web service + free Postgres).
After the first deploy, run `python manage.py createsuperuser` in the Render shell.

Environment variables (see `.env.example`):
- `CONTACT_WHATSAPP` — your number in international format (e.g. 2347000000000) for the "message the founder" link
- `COMMUNITY_LINK` — WhatsApp community invite link shown after signup
- `EARLY_ACCESS_SPOTS` (default 50), `REFERRAL_BOOST` (default 5)
- Custom domain: add it to `ALLOWED_HOSTS` and `https://yourdomain` to `CSRF_TRUSTED_ORIGINS`

## Tracking sources
Add `?utm_source=tiktok` (or `instagram`, `coldemail`, `vendorgroup`…) to links you share; it's saved on each signup so you can see which channel works.
