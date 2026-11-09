from django.urls import path

from . import views

app_name = "waitlist"

urlpatterns = [
    path("", views.index, name="index"),
    path("welcome/<str:code>/", views.thanks, name="thanks"),
]
