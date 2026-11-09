import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Signup


@admin.action(description="Export selected to CSV")
def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="closa_waitlist.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "created_at", "name", "business_name", "email", "whatsapp", "business_type", "country",
        "platforms", "messages_per_day", "willing_to_pay", "referrals", "referred_by", "source", "contacted",
    ])
    for s in queryset:
        writer.writerow([
            s.created_at.strftime("%Y-%m-%d %H:%M"), s.name, s.business_name, s.email, s.whatsapp,
            s.get_business_type_display(), s.country, s.platforms, s.monthly_messages,
            s.willing_to_pay, s.referral_count, s.referred_by.email if s.referred_by else "",
            s.source, s.contacted,
        ])
    return response


@admin.action(description="Mark as contacted")
def mark_contacted(modeladmin, request, queryset):
    queryset.update(contacted=True)


@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = (
        "business_name", "name", "email", "whatsapp", "business_type", "country",
        "willing_to_pay", "referral_total", "source", "contacted", "created_at",
    )
    list_filter = ("business_type", "willing_to_pay", "contacted", "country", "source", "created_at")
    search_fields = ("name", "business_name", "email", "whatsapp", "country")
    readonly_fields = ("referral_code", "created_at")
    list_editable = ("contacted",)
    actions = [export_csv, mark_contacted]
    date_hierarchy = "created_at"

    @admin.display(description="Referrals")
    def referral_total(self, obj):
        return obj.referral_count
