from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Closa admin"
admin.site.site_title = "Closa admin"
admin.site.index_title = "Waitlist"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("waitlist.urls")),
]
