from .base import *  # noqa: F401, F403

DEBUG = False

# ─── Database: SQLite in-memory untuk speed ──────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": True,
    }
}

# ─── Celery: sinkronus, tidak butuh Redis ────────────────────
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# ─── Password hashing: lebih cepat saat test ─────────────────
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# ─── Email ───────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# ─── Skip allauth email verification ─────────────────────────
ACCOUNT_EMAIL_VERIFICATION = "none"

# ─── Static: no manifest ─────────────────────────────────────
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}