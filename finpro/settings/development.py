from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# ─── Debug Toolbar ───────────────────────────────────────────
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

INTERNAL_IPS = ["127.0.0.1"]

# ─── Database (SQLite untuk dev) ─────────────────────────────
# DATABASE_URL di .env = sqlite:///db.sqlite3

# ─── Email: tampilkan di console ─────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ─── Allauth: skip email verification saat dev ───────────────
ACCOUNT_EMAIL_VERIFICATION = "none"

# ─── Tailwind hot reload ─────────────────────────────────────
TAILWIND_DEV_MODE = True
