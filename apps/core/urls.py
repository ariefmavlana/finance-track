from django.urls import path
from django.views.generic import RedirectView

app_name = "core"

urlpatterns = [
    # Root redirect ke dashboard
    path("", RedirectView.as_view(url="/dashboard/", permanent=False), name="home"),
]