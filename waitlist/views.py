from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignupForm
from .models import Signup


def _context(request, **extra):
    ctx = {
        "total_signups": Signup.objects.count(),
        "early_spots": settings.EARLY_ACCESS_SPOTS,
        "contact_whatsapp": settings.CONTACT_WHATSAPP,
    }
    ctx["spots_left"] = max(0, ctx["early_spots"] - ctx["total_signups"])
    ctx.update(extra)
    return ctx


def index(request):
    ref = request.GET.get("ref", "").strip().upper()
    if ref:
        request.session["ref"] = ref
    source = request.GET.get("utm_source", "").strip()[:60]
    if source:
        request.session["source"] = source

    if request.method == "POST":
        form = SignupForm(request.POST)
        email = request.POST.get("email", "").strip().lower()
        existing = Signup.objects.filter(email=email).first() if email else None
        if existing:
            return redirect("waitlist:thanks", code=existing.referral_code)
        if form.is_valid():
            signup = form.save(commit=False)
            ref_code = request.session.get("ref")
            if ref_code:
                signup.referred_by = Signup.objects.filter(referral_code=ref_code).first()
            signup.source = request.session.get("source", "") or ("referral" if signup.referred_by else "")
            signup.save()
            return redirect("waitlist:thanks", code=signup.referral_code)
    else:
        form = SignupForm()

    return render(request, "waitlist/index.html", _context(request, form=form))


def thanks(request, code):
    signup = get_object_or_404(Signup, referral_code=code)
    share_url = request.build_absolute_uri(f"/?ref={signup.referral_code}")
    return render(
        request,
        "waitlist/thanks.html",
        _context(
            request,
            signup=signup,
            share_url=share_url,
            community_link=settings.COMMUNITY_LINK,
            boost=settings.REFERRAL_BOOST,
        ),
    )
