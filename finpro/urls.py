from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),

    # App routes
    path("", include("apps.core.urls", namespace="core")),
    path("", include("apps.accounts.urls", namespace="accounts")),
    path("", include("apps.finance.urls", namespace="finance")),
    path("notifications/", include("apps.notifications.urls", namespace="notifications")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)