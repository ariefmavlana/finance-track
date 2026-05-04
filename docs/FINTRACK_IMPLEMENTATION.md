# FinTrack — Implementation Guide (Awal sampai Selesai)

> **Stack Aktual:** `uv` · `Django 6.0.4` · `HTMX` · `Hyperscript` · `django-tailwind` · `DaisyUI v5`
> **Filosofi:** Hypermedia-first, progressively enhanced, scalable by design.

---

## Daftar Isi

### FASE 1 — Fondasi
- [1.1 Audit & Penyesuaian pyproject.toml](#11-audit--penyesuaian-pyprojecttoml)
- [1.2 Struktur Folder Proyek](#12-struktur-folder-proyek)
- [1.3 Environment Variables (.env)](#13-environment-variables-env)
- [1.4 Django Settings (Bertingkat)](#14-django-settings-bertingkat)
- [1.5 Root URL Configuration](#15-root-url-configuration)

### FASE 2 — Database & Core Models
- [2.1 Abstract Base Models (apps/core)](#21-abstract-base-models-appscore)
- [2.2 Custom User Model (apps/accounts)](#22-custom-user-model-appsaccounts)
- [2.3 Finance Models (apps/finance)](#23-finance-models-appsfinance)
- [2.4 Notifications Model (apps/notifications)](#24-notifications-model-appsnotifications)
- [2.5 Migrasi Database](#25-migrasi-database)

### FASE 3 — Tailwind + DaisyUI Setup
- [3.1 Konfigurasi django-tailwind](#31-konfigurasi-django-tailwind)
- [3.2 Custom Theme FinTrack](#32-custom-theme-fintrack)
- [3.3 Static Files & WhiteNoise](#33-static-files--whitenoise)

### FASE 4 — Template Architecture
- [4.1 Base Template](#41-base-template)
- [4.2 Partial Templates (Navbar, Sidebar, Toast)](#42-partial-templates-navbar-sidebar-toast)
- [4.3 Custom Template Tags](#43-custom-template-tags)
- [4.4 Context Processors](#44-context-processors)

### FASE 5 — Authentication (django-allauth)
- [5.1 Konfigurasi Allauth](#51-konfigurasi-allauth)
- [5.2 Custom Auth Templates](#52-custom-auth-templates)
- [5.3 Profile & Team Views](#53-profile--team-views)

### FASE 6 — Core Mixins & Middleware
- [6.1 View Mixins (HtmxMixin, OwnershipMixin)](#61-view-mixins-htmxmixin-ownershipmixin)
- [6.2 Custom Middleware](#62-custom-middleware)
- [6.3 Permissions Helpers](#63-permissions-helpers)

### FASE 7 — Service Layer & Repository
- [7.1 Transaction Service](#71-transaction-service)
- [7.2 Budget Service](#72-budget-service)
- [7.3 Report Service](#73-report-service)
- [7.4 Import Service (CSV)](#74-import-service-csv)
- [7.5 Currency Service](#75-currency-service)
- [7.6 Transaction Repository](#76-transaction-repository)
- [7.7 Budget Repository](#77-budget-repository)

### FASE 8 — Forms
- [8.1 Transaction Form](#81-transaction-form)
- [8.2 Budget Form](#82-budget-form)
- [8.3 Account Form](#83-account-form)
- [8.4 Import Form (CSV)](#84-import-form-csv)

### FASE 9 — Views & URL Routing
- [9.1 Finance URL Config](#91-finance-url-config)
- [9.2 Dashboard Views](#92-dashboard-views)
- [9.3 Transaction Views](#93-transaction-views)
- [9.4 Budget Views](#94-budget-views)
- [9.5 Account Views](#95-account-views)
- [9.6 Report Views](#96-report-views)

### FASE 10 — Templates Finance
- [10.1 Dashboard Template](#101-dashboard-template)
- [10.2 Transaction List & Partials](#102-transaction-list--partials)
- [10.3 Budget Templates](#103-budget-templates)
- [10.4 Account Templates](#104-account-templates)
- [10.5 Report Templates](#105-report-templates)

### FASE 11 — HTMX Patterns
- [11.1 Infinite Scroll](#111-infinite-scroll)
- [11.2 Inline Edit](#112-inline-edit)
- [11.3 OOB Swaps](#113-oob-swaps)
- [11.4 Live Search & Filter](#114-live-search--filter)
- [11.5 Polling Dashboard](#115-polling-dashboard)

### FASE 12 — Celery & Background Tasks
- [12.1 Instalasi & Konfigurasi Celery](#121-instalasi--konfigurasi-celery)
- [12.2 Recurring Transaction Task](#122-recurring-transaction-task)
- [12.3 Exchange Rate Task](#123-exchange-rate-task)
- [12.4 Budget Alert Task](#124-budget-alert-task)

### FASE 13 — Caching & Performance
- [13.1 Redis Cache Setup](#131-redis-cache-setup)
- [13.2 View-level & Query-level Cache](#132-view-level--query-level-cache)
- [13.3 QuerySet Optimization](#133-queryset-optimization)

### FASE 14 — Notifications
- [14.1 Notification Model & Service](#141-notification-model--service)
- [14.2 In-app Notification Views](#142-in-app-notification-views)
- [14.3 Email Notification](#143-email-notification)

### FASE 15 — Testing
- [15.1 Setup pytest-django](#151-setup-pytest-django)
- [15.2 Factories (factory-boy)](#152-factories-factory-boy)
- [15.3 Unit Tests](#153-unit-tests)
- [15.4 Integration Tests (HTMX)](#154-integration-tests-htmx)

### FASE 16 — Security
- [16.1 Django Security Settings](#161-django-security-settings)
- [16.2 HTMX Security Middleware](#162-htmx-security-middleware)
- [16.3 Rate Limiting](#163-rate-limiting)
- [16.4 CSP Headers](#164-csp-headers)

### FASE 17 — Deployment
- [17.1 Dockerfile & Docker Compose](#171-dockerfile--docker-compose)
- [17.2 Nginx Configuration](#172-nginx-configuration)
- [17.3 Production Settings](#173-production-settings)
- [17.4 CI/CD GitHub Actions](#174-cicd-github-actions)

### FASE 18 — Monitoring
- [18.1 Sentry Integration](#181-sentry-integration)
- [18.2 Health Check Endpoint](#182-health-check-endpoint)

---

## FASE 1 — Fondasi

### 1.1 Audit & Penyesuaian pyproject.toml

pyproject.toml kamu sudah memiliki beberapa dependencies inti. Berikut adalah **versi lengkap** yang perlu diupdate untuk mendukung seluruh fitur FinTrack. Jalankan perintah `uv add` untuk setiap package yang belum ada.

```toml
# pyproject.toml — VERSI LENGKAP
[project]
name = "finance-track"
version = "0.1.0"
description = "Hypermedia-first personal finance tracker"
readme = "README.md"
requires-python = ">=3.12"

dependencies = [
    # ── Core Django ──────────────────────────────────────────
    "django>=6.0.4",
    "django-environ>=0.11",

    # ── Database ─────────────────────────────────────────────
    "psycopg[binary]>=3.2",          # PostgreSQL driver (wajib untuk prod)

    # ── Cache & Task Queue ────────────────────────────────────
    "redis>=5.0",
    "celery[redis]>=5.4",
    "django-celery-beat>=2.7",
    "django-celery-results>=2.5",

    # ── Auth ─────────────────────────────────────────────────
    "django-allauth[socialaccount]>=65.16.1",

    # ── HTMX Helper ──────────────────────────────────────────
    "django-htmx>=1.21",

    # ── Frontend ─────────────────────────────────────────────
    "django-tailwind>=4.4.2",        # sudah ada
    "django-widget-tweaks>=1.5.1",   # sudah ada

    # ── Forms & Filter ───────────────────────────────────────
    "django-filter>=25.2",           # sudah ada

    # ── Storage & Files ──────────────────────────────────────
    "django-storages[s3]>=1.14",
    "Pillow>=11.0",

    # ── Export ───────────────────────────────────────────────
    "openpyxl>=3.1",
    "reportlab>=4.2",

    # ── Utilities ────────────────────────────────────────────
    "django-model-utils>=5.0",
    "django-extensions>=4.1",         # sudah ada
    "whitenoise>=6.7",                # static file serving

    # ── Security ─────────────────────────────────────────────
    "django-csp>=4.0",
    "django-ratelimit>=4.1",

    # ── Monitoring ───────────────────────────────────────────
    "sentry-sdk[django]>=2.0",
    "django-health-check>=3.18",

    # ── Already installed ────────────────────────────────────
    "django-debug-toolbar>=6.3.0",
    "faker>=40.15.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-django>=4.9",
    "pytest-cov>=5.0",
    "pytest-xdist>=3.6",
    "factory-boy>=3.3",
    "playwright>=1.47",
    "pytest-playwright>=0.5",
    "ipython>=8.0",
    "pre-commit>=3.8",
    "ruff>=0.6",
    "mypy>=1.11",
    "django-stubs[compatible-mypy]>=5.1",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "S"]
ignore = []

[tool.mypy]
plugins = ["mypy_django_plugin.main"]
strict = true

[tool.django-stubs]
django_settings_module = "config.settings.development"

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
python_files = ["tests.py", "test_*.py", "*_test.py"]
addopts = "--cov=apps --cov-report=term-missing --cov-fail-under=80"
```

**Perintah install semua dependencies baru sekaligus:**

```bash
uv add django-environ psycopg "psycopg[binary]" redis "celery[redis]" \
    django-celery-beat django-celery-results "django-allauth[socialaccount]" \
    django-htmx "django-storages[s3]" Pillow openpyxl reportlab \
    django-model-utils whitenoise django-csp django-ratelimit \
    "sentry-sdk[django]" django-health-check

uv add --group dev pytest pytest-django pytest-cov pytest-xdist \
    factory-boy playwright pytest-playwright ipython pre-commit ruff mypy \
    "django-stubs[compatible-mypy]"
```

---

### 1.2 Struktur Folder Proyek

Buat seluruh struktur folder ini dari root proyek kamu. Jalankan satu per satu:

```bash
# Dari root direktori proyek (finance-track/)

# Finpro
mkdir -p finpro/settings

# Apps
mkdir -p apps/core/templatetags
mkdir -p apps/core/utils
mkdir -p apps/accounts/services
mkdir -p apps/accounts/templates/accounts
mkdir -p apps/finance/models
mkdir -p apps/finance/views
mkdir -p apps/finance/forms
mkdir -p apps/finance/services
mkdir -p apps/finance/repositories
mkdir -p apps/finance/templates/finance/transactions
mkdir -p apps/finance/templates/finance/budgets
mkdir -p apps/finance/templates/finance/accounts
mkdir -p apps/finance/templates/finance/reports
mkdir -p apps/finance/templates/finance/dashboard
mkdir -p apps/notifications/templates/notifications

# Global templates
mkdir -p templates/partials
mkdir -p templates/errors

# Static
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images

# Tests
mkdir -p tests/factories
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/e2e

# Docker
mkdir -p docker/nginx

# Locale
mkdir -p locale
```

**Buat `__init__.py` di setiap folder Python:**

```bash
touch finpro/__init__.py
touch finpro/settings/__init__.py
touch apps/__init__.py
touch apps/core/__init__.py
touch apps/core/templatetags/__init__.py
touch apps/core/utils/__init__.py
touch apps/accounts/__init__.py
touch apps/accounts/services/__init__.py
touch apps/finance/__init__.py
touch apps/finance/models/__init__.py
touch apps/finance/views/__init__.py
touch apps/finance/forms/__init__.py
touch apps/finance/services/__init__.py
touch apps/finance/repositories/__init__.py
touch apps/notifications/__init__.py
touch tests/__init__.py
touch tests/factories/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
touch tests/e2e/__init__.py
```

**Struktur lengkap yang diharapkan:**

```
finance-track/
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
├── .env                         ← gitignored
├── manage.py
│
├── finpro/
│   ├── __init__.py
│   ├── celery.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── middleware.py
│   │   ├── mixins.py
│   │   ├── permissions.py
│   │   ├── context_processors.py
│   │   ├── urls.py
│   │   ├── templatetags/
│   │   │   ├── __init__.py
│   │   │   ├── htmx_tags.py
│   │   │   └── finance_tags.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── currency.py
│   │       └── dates.py
│   │
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── auth_service.py
│   │   └── templates/accounts/
│   │       ├── profile.html
│   │       └── team.html
│   │
│   ├── finance/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── signals.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── account.py
│   │   │   ├── category.py
│   │   │   ├── transaction.py
│   │   │   ├── budget.py
│   │   │   └── recurring.py
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py
│   │   │   ├── transactions.py
│   │   │   ├── budgets.py
│   │   │   ├── accounts.py
│   │   │   └── reports.py
│   │   ├── forms/
│   │   │   ├── __init__.py
│   │   │   ├── transaction_form.py
│   │   │   ├── budget_form.py
│   │   │   ├── account_form.py
│   │   │   └── import_form.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── transaction_service.py
│   │   │   ├── budget_service.py
│   │   │   ├── report_service.py
│   │   │   ├── import_service.py
│   │   │   └── currency_service.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── transaction_repo.py
│   │   │   └── budget_repo.py
│   │   └── templates/finance/
│   │       ├── dashboard/
│   │       │   ├── index.html
│   │       │   └── _kpi_cards.html
│   │       ├── transactions/
│   │       │   ├── list.html
│   │       │   ├── detail.html
│   │       │   ├── _form.html
│   │       │   ├── _row.html
│   │       │   ├── _list_partial.html
│   │       │   └── _filters.html
│   │       ├── budgets/
│   │       │   ├── list.html
│   │       │   └── _form.html
│   │       ├── accounts/
│   │       │   ├── list.html
│   │       │   └── detail.html
│   │       └── reports/
│   │           └── index.html
│   │
│   └── notifications/
│       ├── __init__.py
│       ├── models.py
│       ├── services.py
│       ├── tasks.py
│       ├── views.py
│       ├── urls.py
│       └── templates/notifications/
│           └── _notification_item.html
│
├── static/
│   ├── css/
│   │   └── app.css
│   ├── js/
│   │   ├── htmx.min.js          ← download manual
│   │   ├── hyperscript.min.js   ← download manual
│   │   └── fintrack.js
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── partials/
│   │   ├── _navbar.html
│   │   ├── _sidebar.html
│   │   ├── _toast.html
│   │   ├── _breadcrumb.html
│   │   └── _pagination.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── factories/
│   │   └── __init__.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
└── docker/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── docker-compose.prod.yml
    └── nginx/
        └── nginx.conf
```

**Download HTMX dan Hyperscript:**

```bash
# HTMX v2.x
curl -L https://unpkg.com/htmx.org@2.0.10/dist/htmx.min.js -o static/js/htmx.min.js

# Hyperscript v0.9.x
curl -L https://unpkg.com/hyperscript.org@0.9.91/dist/_hyperscript.min.js -o static/js/hyperscript.min.js
```

---

### 1.3 Environment Variables (.env)

**Buat file `.env.example`:**

```ini
# .env.example

# ── Django Core ──────────────────────────────────────────────
DJANGO_SECRET_KEY=change-me-to-a-very-long-random-string-50-chars-min
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=config.settings.development
DJANGO_ENV=development

# ── Database ─────────────────────────────────────────────────
# SQLite untuk development (default):
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL untuk production:
# DATABASE_URL=postgres://fintrack:password@localhost:5432/fintrack_db

# ── Cache & Celery ───────────────────────────────────────────
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# ── Email ────────────────────────────────────────────────────
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@fintrack.app
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# ── Storage (Production S3) ──────────────────────────────────
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=ap-southeast-1

# ── OAuth ────────────────────────────────────────────────────
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# ── External APIs ────────────────────────────────────────────
EXCHANGERATE_API_KEY=

# ── Sentry ───────────────────────────────────────────────────
SENTRY_DSN=

# ── Security (production = True) ─────────────────────────────
DJANGO_SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**Salin ke `.env` dan isi nilainya:**

```bash
cp .env.example .env
```

---

### 1.4 Django Settings (Bertingkat)

#### `config/settings/base.py`

```python
"""
Base settings — shared across all environments.
JANGAN import langsung file ini; import child settings.
"""
from pathlib import Path
import environ

env = environ.Env(
    DEBUG=(bool, False),
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Baca .env file
environ.Env.read_env(BASE_DIR / ".env")

# ─── Core ────────────────────────────────────────────────────
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost"])

# ─── Apps ────────────────────────────────────────────────────
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    # Auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # HTMX
    "django_htmx",
    # Frontend
    "tailwind",
    "widget_tweaks",
    # Filter
    "django_filters",
    # Celery
    "django_celery_beat",
    "django_celery_results",
    # Health
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.celery",
    # Utilities
    "django_extensions",
]

LOCAL_APPS = [
    "apps.core",
    "apps.accounts",
    "apps.finance",
    "apps.notifications",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ─── Tailwind App Name ────────────────────────────────────────
TAILWIND_APP_NAME = "theme"      # django-tailwind buat app ini secara otomatis

# ─── Middleware ───────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "apps.core.middleware.TimezoneMiddleware",
    "apps.core.middleware.CurrentUserMiddleware",
]

ROOT_URLCONF = "config.urls"

# ─── Templates ───────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.global_context",
            ],
        },
    },
]

# ─── Database ────────────────────────────────────────────────
DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR}/db.sqlite3")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = 60

# ─── Auth ────────────────────────────────────────────────────
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# ─── Allauth ─────────────────────────────────────────────────
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# ─── Celery ──────────────────────────────────────────────────
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/1")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="django-db")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_BEAT_SCHEDULE = {
    "generate-recurring-transactions": {
        "task": "finance.generate_recurring_transactions",
        "schedule": "0 1 * * *",
    },
    "refresh-exchange-rates": {
        "task": "finance.refresh_exchange_rates",
        "schedule": "0 */6 * * *",
    },
}

# ─── Static & Media ──────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ─── Internationalization ────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ─── Default PK ──────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── Logging ─────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "WARNING"},
        "apps": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
}

# ─── Finance App Config ──────────────────────────────────────
FINTRACK_BASE_CURRENCY = "IDR"
FINTRACK_SUPPORTED_CURRENCIES = ["IDR", "USD", "EUR", "SGD", "JPY"]
FINTRACK_EXCHANGE_RATE_REFRESH_HOURS = 6

# ─── Email ───────────────────────────────────────────────────
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@fintrack.app")
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
```

#### `config/settings/development.py`

```python
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
```

#### `config/settings/testing.py`

```python
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
```

#### `config/settings/production.py`

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .base import *  # noqa: F401, F403
import environ

env = environ.Env()

DEBUG = False

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# ─── HTTPS Security ──────────────────────────────────────────
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ─── Cache: Redis ────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "KEY_PREFIX": "fintrack",
        "TIMEOUT": 300,
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# ─── Database: PostgreSQL ────────────────────────────────────
DATABASES = {
    "default": env.db("DATABASE_URL")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = 60

# ─── Storage: S3 ─────────────────────────────────────────────
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="ap-southeast-1")
AWS_DEFAULT_ACL = "private"

if AWS_STORAGE_BUCKET_NAME:
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        },
    }

# ─── Sentry ──────────────────────────────────────────────────
SENTRY_DSN = env("SENTRY_DSN", default="")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(transaction_style="url"),
            CeleryIntegration(monitor_beat_tasks=True),
            RedisIntegration(),
        ],
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
        send_default_pii=False,
        environment=env("DJANGO_ENV", default="production"),
    )

# ─── CSP ─────────────────────────────────────────────────────
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'",)
```

---

### 1.5 Root URL Configuration

#### `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("health/", include("health_check.urls")),

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
```

#### `config/wsgi.py`

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
application = get_wsgi_application()
```

#### `config/asgi.py`

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
application = get_asgi_application()
```

#### `config/celery.py`

```python
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("fintrack")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
```

#### `config/__init__.py`

```python
# Pastikan Celery dimuat saat Django start
from .celery import app as celery_app

__all__ = ("celery_app",)
```

#### `manage.py` (di root proyek)

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
```

---

## FASE 2 — Database & Core Models

### 2.1 Abstract Base Models (apps/core)

#### `apps/core/models.py`

```python
import uuid
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base: created_at + updated_at di setiap model."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base: UUID sebagai primary key."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    """Manager default: hanya tampilkan record yang belum dihapus."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    """Abstract base: soft delete (tandai deleted_at) bukan hard delete."""
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()   # Termasuk yang sudah dihapus

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel, SoftDeleteModel):
    """
    Model dasar untuk semua domain model.
    Gabungkan UUID PK + timestamps + soft delete.
    """
    class Meta:
        abstract = True
```

#### `apps/core/urls.py`

```python
from django.urls import path
from django.views.generic import RedirectView

app_name = "core"

urlpatterns = [
    # Root redirect ke dashboard
    path("", RedirectView.as_view(url="/dashboard/", permanent=False), name="home"),
]
```

#### `apps/core/context_processors.py`

```python
from django.conf import settings


def global_context(request):
    """Context processor: tersedia di semua template."""
    ctx = {
        "debug": settings.DEBUG,
        "base_currency": settings.FINTRACK_BASE_CURRENCY,
        "supported_currencies": settings.FINTRACK_SUPPORTED_CURRENCIES,
    }
    if request.user.is_authenticated:
        ctx["user_timezone"] = request.user.timezone
    return ctx
```

---

### 2.2 Custom User Model (apps/accounts)

#### `apps/accounts/models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """Custom user model dengan kolom tambahan."""
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    timezone = models.CharField(max_length=50, default="Asia/Jakarta")
    base_currency = models.CharField(max_length=3, default="IDR")
    is_onboarded = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email


class Team(TimeStampedModel):
    """Workspace bersama untuk finance tracking keluarga/tim."""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_teams"
    )
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "accounts_team"

    def __str__(self) -> str:
        return self.name


class TeamMembership(TimeStampedModel):
    ROLE_VIEWER = "viewer"
    ROLE_EDITOR = "editor"
    ROLE_ADMIN = "admin"
    ROLES = [
        (ROLE_VIEWER, "Viewer"),
        (ROLE_EDITOR, "Editor"),
        (ROLE_ADMIN, "Admin"),
    ]

    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=ROLES, default=ROLE_VIEWER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts_team_membership"
        unique_together = [("team", "user")]

    def __str__(self) -> str:
        return f"{self.user.email} in {self.team.name} ({self.role})"
```

#### `apps/accounts/admin.py`

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Team, TeamMembership


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username", "is_onboarded", "base_currency", "created_at"]
    search_fields = ["email", "username"]
    list_filter = ["is_onboarded", "base_currency"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("FinTrack", {"fields": ("avatar", "timezone", "base_currency", "is_onboarded")}),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "slug"]
    search_fields = ["name", "slug"]


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ["team", "user", "role", "joined_at"]
    list_filter = ["role"]
```

#### `apps/accounts/urls.py`

```python
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.ProfileUpdateView.as_view(), name="profile"),
    path("team/", views.TeamView.as_view(), name="team"),
]
```

#### `apps/accounts/forms.py`

```python
from django import forms
from .models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "avatar", "timezone", "base_currency"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "first_name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "last_name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "timezone": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "base_currency": forms.Select(
                attrs={"class": "select select-bordered w-full"},
                choices=[
                    ("IDR", "IDR — Rupiah"),
                    ("USD", "USD — US Dollar"),
                    ("EUR", "EUR — Euro"),
                    ("SGD", "SGD — Singapore Dollar"),
                    ("JPY", "JPY — Japanese Yen"),
                ],
            ),
        }
```

#### `apps/accounts/views.py`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import User
from .forms import UserProfileForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user


class TeamView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/team.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["owned_teams"] = self.request.user.owned_teams.all()
        ctx["memberships"] = self.request.user.memberships.select_related("team").all()
        return ctx
```

---

### 2.3 Finance Models (apps/finance)

#### `apps/finance/models/__init__.py`

```python
from .account import FinancialAccount
from .category import Category
from .transaction import Transaction, Tag
from .budget import Budget
from .recurring import RecurringTransaction

__all__ = [
    "FinancialAccount",
    "Category",
    "Transaction",
    "Tag",
    "Budget",
    "RecurringTransaction",
]
```

#### `apps/finance/models/account.py`

```python
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel

User = get_user_model()


class FinancialAccount(BaseModel):
    TYPE_BANK = "bank"
    TYPE_CASH = "cash"
    TYPE_CREDIT_CARD = "credit_card"
    TYPE_INVESTMENT = "investment"
    TYPE_LOAN = "loan"
    TYPE_E_WALLET = "e_wallet"

    ACCOUNT_TYPES = [
        (TYPE_BANK, "Bank Account"),
        (TYPE_CASH, "Cash"),
        (TYPE_CREDIT_CARD, "Credit Card"),
        (TYPE_INVESTMENT, "Investment"),
        (TYPE_LOAN, "Loan"),
        (TYPE_E_WALLET, "E-Wallet"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="financial_accounts"
    )
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    currency = models.CharField(max_length=3, default="IDR")
    initial_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    current_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    color = models.CharField(max_length=7, default="#3B82F6")
    icon = models.CharField(max_length=50, default="wallet")
    is_active = models.BooleanField(default=True)
    institution_name = models.CharField(max_length=100, blank=True)
    last_four_digits = models.CharField(max_length=4, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "finance_financial_account"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_account_type_display()})"
```

#### `apps/finance/models/category.py`

```python
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel

User = get_user_model()


class Category(BaseModel):
    TYPE_INCOME = "income"
    TYPE_EXPENSE = "expense"
    TYPE_TRANSFER = "transfer"

    CATEGORY_TYPES = [
        (TYPE_INCOME, "Income"),
        (TYPE_EXPENSE, "Expense"),
        (TYPE_TRANSFER, "Transfer"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="categories",
        null=True, blank=True,
    )
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    icon = models.CharField(max_length=50, default="tag")
    color = models.CharField(max_length=7, default="#6B7280")
    is_system = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="subcategories",
    )

    class Meta:
        db_table = "finance_category"
        verbose_name_plural = "categories"
        ordering = ["name"]
        unique_together = [("user", "name", "parent")]

    def __str__(self) -> str:
        return self.name
```

#### `apps/finance/models/transaction.py`

```python
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.core.models import BaseModel
from .account import FinancialAccount
from .category import Category

User = get_user_model()


class Tag(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#9CA3AF")

    class Meta:
        db_table = "finance_tag"
        unique_together = [("user", "name")]

    def __str__(self) -> str:
        return self.name


class Transaction(BaseModel):
    TYPE_INCOME = "income"
    TYPE_EXPENSE = "expense"
    TYPE_TRANSFER = "transfer"

    TRANSACTION_TYPES = [
        (TYPE_INCOME, "Income"),
        (TYPE_EXPENSE, "Expense"),
        (TYPE_TRANSFER, "Transfer"),
    ]

    STATUS_PENDING = "pending"
    STATUS_CLEARED = "cleared"
    STATUS_RECONCILED = "reconciled"

    STATUSES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CLEARED, "Cleared"),
        (STATUS_RECONCILED, "Reconciled"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    account = models.ForeignKey(
        FinancialAccount, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="transactions"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="transactions")
    transfer_to_account = models.ForeignKey(
        FinancialAccount, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="incoming_transfers"
    )

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    currency = models.CharField(max_length=3)
    amount_in_base_currency = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    exchange_rate = models.DecimalField(
        max_digits=10, decimal_places=6, null=True, blank=True
    )

    date = models.DateField(db_index=True)
    description = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    payee = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=15, choices=STATUSES, default=STATUS_CLEARED)
    reference_number = models.CharField(max_length=100, blank=True)
    receipt_image = models.ImageField(
        upload_to="receipts/%Y/%m/", blank=True, null=True
    )
    is_recurring_instance = models.BooleanField(default=False)
    recurring_transaction = models.ForeignKey(
        "finance.RecurringTransaction", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="instances"
    )

    class Meta:
        db_table = "finance_transaction"
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "category"]),
            models.Index(fields=["user", "transaction_type"]),
            models.Index(fields=["account", "date"]),
            models.Index(
                fields=["user", "deleted_at"],
                name="active_transactions_idx",
                condition=models.Q(deleted_at__isnull=True),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.description} — {self.amount} {self.currency} ({self.date})"

    @property
    def is_expense(self) -> bool:
        return self.transaction_type == self.TYPE_EXPENSE

    @property
    def is_income(self) -> bool:
        return self.transaction_type == self.TYPE_INCOME
```

#### `apps/finance/models/budget.py`

```python
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel
from .category import Category

User = get_user_model()


class Budget(BaseModel):
    PERIOD_WEEKLY = "weekly"
    PERIOD_MONTHLY = "monthly"
    PERIOD_QUARTERLY = "quarterly"
    PERIOD_YEARLY = "yearly"
    PERIOD_CUSTOM = "custom"

    PERIODS = [
        (PERIOD_WEEKLY, "Weekly"),
        (PERIOD_MONTHLY, "Monthly"),
        (PERIOD_QUARTERLY, "Quarterly"),
        (PERIOD_YEARLY, "Yearly"),
        (PERIOD_CUSTOM, "Custom"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="budgets"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    period = models.CharField(max_length=10, choices=PERIODS, default=PERIOD_MONTHLY)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    alert_at_percentage = models.PositiveSmallIntegerField(default=80)
    alert_sent = models.BooleanField(default=False)

    class Meta:
        db_table = "finance_budget"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} — {self.amount} {self.currency}/{self.period}"
```

#### `apps/finance/models/recurring.py`

```python
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel
from .account import FinancialAccount
from .category import Category

User = get_user_model()


class RecurringTransaction(BaseModel):
    FREQ_DAILY = "daily"
    FREQ_WEEKLY = "weekly"
    FREQ_BIWEEKLY = "biweekly"
    FREQ_MONTHLY = "monthly"
    FREQ_QUARTERLY = "quarterly"
    FREQ_YEARLY = "yearly"

    FREQUENCIES = [
        (FREQ_DAILY, "Daily"),
        (FREQ_WEEKLY, "Weekly"),
        (FREQ_BIWEEKLY, "Bi-weekly"),
        (FREQ_MONTHLY, "Monthly"),
        (FREQ_QUARTERLY, "Quarterly"),
        (FREQ_YEARLY, "Yearly"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recurring_transactions"
    )
    account = models.ForeignKey(
        FinancialAccount, on_delete=models.CASCADE, related_name="recurring_transactions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="recurring_transactions"
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=[("income", "Income"), ("expense", "Expense")],
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    frequency = models.CharField(max_length=10, choices=FREQUENCIES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_due_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "finance_recurring_transaction"
        ordering = ["next_due_date"]

    def __str__(self) -> str:
        return f"{self.description} ({self.frequency})"

    def advance_next_due_date(self):
        """Maju ke tanggal berikutnya sesuai frekuensi."""
        from dateutil.relativedelta import relativedelta
        import datetime

        freq_map = {
            self.FREQ_DAILY: datetime.timedelta(days=1),
            self.FREQ_WEEKLY: datetime.timedelta(weeks=1),
            self.FREQ_BIWEEKLY: datetime.timedelta(weeks=2),
            self.FREQ_MONTHLY: relativedelta(months=1),
            self.FREQ_QUARTERLY: relativedelta(months=3),
            self.FREQ_YEARLY: relativedelta(years=1),
        }
        delta = freq_map.get(self.frequency)
        if delta:
            self.next_due_date = self.next_due_date + delta
            self.save(update_fields=["next_due_date"])
```

#### `apps/finance/admin.py`

```python
from django.contrib import admin
from .models import FinancialAccount, Category, Transaction, Tag, Budget, RecurringTransaction


@admin.register(FinancialAccount)
class FinancialAccountAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "account_type", "currency", "current_balance", "is_active"]
    list_filter = ["account_type", "currency", "is_active"]
    search_fields = ["name", "user__email"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category_type", "user", "is_system", "parent"]
    list_filter = ["category_type", "is_system"]
    search_fields = ["name"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["description", "user", "amount", "currency", "transaction_type", "date", "status"]
    list_filter = ["transaction_type", "status", "currency"]
    search_fields = ["description", "payee", "user__email"]
    date_hierarchy = "date"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "color"]
    search_fields = ["name"]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "category", "amount", "currency", "period", "is_active"]
    list_filter = ["period", "is_active"]
    search_fields = ["name", "user__email"]


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ["description", "user", "amount", "frequency", "next_due_date", "is_active"]
    list_filter = ["frequency", "is_active"]
    search_fields = ["description"]
```

---

### 2.4 Notifications Model (apps/notifications)

#### `apps/notifications/models.py`

```python
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()


class Notification(TimeStampedModel):
    TYPE_BUDGET_ALERT = "budget_alert"
    TYPE_LARGE_TRANSACTION = "large_transaction"
    TYPE_RECURRING = "recurring"
    TYPE_SYSTEM = "system"

    TYPES = [
        (TYPE_BUDGET_ALERT, "Budget Alert"),
        (TYPE_LARGE_TRANSACTION, "Large Transaction"),
        (TYPE_RECURRING, "Recurring Transaction"),
        (TYPE_SYSTEM, "System"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=20, choices=TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    url = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "notifications_notification"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.notification_type}: {self.title} ({self.user.email})"
```

#### `apps/notifications/urls.py`

```python
from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="list"),
    path("<int:pk>/read/", views.MarkReadView.as_view(), name="mark-read"),
    path("read-all/", views.MarkAllReadView.as_view(), name="mark-all-read"),
]
```

---

### 2.5 Migrasi Database

Setelah semua model dibuat, jalankan migrasi:

```bash
# Buat migrasi untuk semua app
uv run python manage.py makemigrations core
uv run python manage.py makemigrations accounts
uv run python manage.py makemigrations finance
uv run python manage.py makemigrations notifications

# Jalankan migrasi
uv run python manage.py migrate

# Buat superuser
uv run python manage.py createsuperuser
```

**Catatan penting untuk urutan migrasi:** `accounts` harus dimigrasikan sebelum `finance` karena `finance` memiliki FK ke `User`. Django biasanya menangani ini secara otomatis, tapi jika ada error dependency, jalankan `makemigrations` satu per satu seperti di atas.

---

## FASE 3 — Tailwind + DaisyUI Setup

### 3.1 Konfigurasi django-tailwind

`django-tailwind` berbeda dari Tailwind raw — ia menggunakan Node.js di belakang layar untuk membangun CSS.

**Langkah 1: Pastikan Node.js terinstall**

```bash
node --version   # harus >= 18
npm --version
```

**Langkah 2: Inisialisasi django-tailwind**

```bash
# Buat app Tailwind (akan membuat folder 'theme/')
uv run python manage.py tailwind init

# Jalankan saat ditanya "app name": ketik 'theme'
```

**Langkah 3: Tambahkan 'theme' ke INSTALLED_APPS di base.py**

```python
# Sudah ada di base.py di atas:
# "tailwind",
# Tambahkan juga:
INSTALLED_APPS += ["theme"]  # ← tambahkan ke THIRD_PARTY_APPS
```

**Atau lebih baik, di base.py:**

```python
THIRD_PARTY_APPS = [
    ...
    "tailwind",
    "theme",          # ← app yang dihasilkan oleh `tailwind init`
    ...
]
```

**Langkah 4: Install Node dependencies**

```bash
uv run python manage.py tailwind install
```

**Langkah 5: Jalankan Tailwind watcher (saat development)**

```bash
# Terminal terpisah
uv run python manage.py tailwind start
```

---

### 3.2 Custom Theme FinTrack

Setelah `tailwind init`, akan ada file `theme/static_src/src/styles.css`. Edit file tersebut:

#### `theme/static_src/src/styles.css`

```css
@import "tailwindcss";

/* ─── Import DaisyUI ────────────────────────────────────────── */
@plugin "daisyui";

/* ─── Custom FinTrack Theme ─────────────────────────────────── */
@plugin "daisyui" {
  themes: [
    {
      fintrack: {
        "primary": "#2563EB",
        "primary-content": "#FFFFFF",
        "secondary": "#7C3AED",
        "secondary-content": "#FFFFFF",
        "accent": "#059669",
        "accent-content": "#FFFFFF",
        "neutral": "#374151",
        "neutral-content": "#F9FAFB",
        "base-100": "#FFFFFF",
        "base-200": "#F3F4F6",
        "base-300": "#E5E7EB",
        "base-content": "#111827",
        "info": "#0EA5E9",
        "success": "#10B981",
        "warning": "#F59E0B",
        "error": "#EF4444",
      }
    },
    "dark",
  ];
}

/* ─── Custom Utilities ──────────────────────────────────────── */
@layer utilities {
  .currency {
    font-variant-numeric: tabular-nums;
    font-feature-settings: "tnum";
  }

  .income {
    @apply text-success font-semibold currency;
  }

  .expense {
    @apply text-error font-semibold currency;
  }
}

/* ─── HTMX Loading Indicator ────────────────────────────────── */
.htmx-indicator {
  opacity: 0;
  transition: opacity 200ms ease-in;
}
.htmx-request .htmx-indicator,
.htmx-request.htmx-indicator {
  opacity: 1;
}

/* ─── View Transitions ──────────────────────────────────────── */
@view-transition {
  navigation: auto;
}
::view-transition-old(main-content) {
  animation: 200ms ease-out both fade-out;
}
::view-transition-new(main-content) {
  animation: 300ms ease-in both fade-in;
}
@keyframes fade-out {
  from { opacity: 1; transform: translateY(0); }
  to   { opacity: 0; transform: translateY(-8px); }
}
@keyframes fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

**Install DaisyUI sebagai Node package:**

```bash
cd theme/static_src
npm install daisyui@latest
cd ../../
```

---

### 3.3 Static Files & WhiteNoise

WhiteNoise sudah dikonfigurasi di `base.py`. Pastikan `manage.py collectstatic` berjalan sebelum deploy:

```bash
# Development: tidak perlu collectstatic, DEBUG=True menggunakan STATICFILES_DIRS
# Production:
uv run python manage.py collectstatic --noinput
```

---

## FASE 4 — Template Architecture

### 4.1 Base Template

#### `templates/base.html`

```html
{% load static %}
<!DOCTYPE html>
<html lang="en" data-theme="fintrack" class="h-full">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{% block title %}FinTrack{% endblock %}</title>

  {% if debug %}
    {# Dev: CDN DaisyUI + Tailwind (tidak perlu build) #}
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5/dist/full.min.css" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com"></script>
  {% else %}
    {# Prod: compiled CSS dari django-tailwind #}
    {% load tailwind_tags %}
    {% tailwind_css %}
  {% endif %}

  {# HTMX #}
  <script src="{% static 'js/htmx.min.js' %}" defer></script>
  {# Hyperscript #}
  <script src="{% static 'js/hyperscript.min.js' %}" defer></script>

  {# HTMX global config #}
  <meta name="htmx-config" content='{"globalViewTransitions": true, "defaultSwapStyle": "innerHTML"}' />

  {# CSRF untuk HTMX #}
  <meta name="csrf-token" content="{{ csrf_token }}" />

  {% block extra_head %}{% endblock %}
</head>

<body
  class="h-full bg-base-200"
  hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
>
  {# Toast container — updated via OOB swaps #}
  <div id="toast-container" class="toast toast-top toast-end z-50">
    {% include "partials/_toast.html" %}
  </div>

  {% if user.is_authenticated %}
    <div class="flex h-full">
      {% include "partials/_sidebar.html" %}

      <div class="flex-1 flex flex-col overflow-hidden">
        {% include "partials/_navbar.html" %}

        <main
          id="main-content"
          class="flex-1 overflow-y-auto p-6"
          style="view-transition-name: main-content;"
        >
          {% block content %}{% endblock %}
        </main>
      </div>
    </div>
  {% else %}
    <div class="min-h-screen flex items-center justify-center bg-base-200">
      {% block auth_content %}{% endblock %}
    </div>
  {% endif %}

  {# Django messages → toast OOB #}
  {% if messages %}
    {% for message in messages %}
      <div id="toast-container" hx-swap-oob="beforeend">
        <div
          class="alert alert-{{ message.tags }} shadow-lg mb-2 transition-all duration-500"
          _="on load wait 3.5s then add .opacity-0 .translate-x-full then wait 500ms then remove me"
        >
          <span>{{ message }}</span>
        </div>
      </div>
    {% endfor %}
  {% endif %}

  {# FinTrack custom JS #}
  <script src="{% static 'js/fintrack.js' %}"></script>

  {% block extra_scripts %}{% endblock %}
</body>
</html>
```

---

### 4.2 Partial Templates (Navbar, Sidebar, Toast)

#### `templates/partials/_sidebar.html`

```html
{% load static %}
<aside class="w-64 bg-base-100 shadow-lg flex flex-col h-full">
  {# Logo #}
  <div class="p-4 border-b border-base-300">
    <a href="{% url 'finance:dashboard' %}" class="flex items-center gap-2">
      <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
        <span class="text-white font-bold text-sm">FT</span>
      </div>
      <span class="font-bold text-xl text-base-content">FinTrack</span>
    </a>
  </div>

  {# Navigation #}
  <nav class="flex-1 p-4 space-y-1">
    <a href="{% url 'finance:dashboard' %}"
       class="flex items-center gap-3 px-3 py-2 rounded-lg
              hover:bg-base-200 transition-colors
              {% if request.resolver_match.url_name == 'dashboard' %}bg-primary/10 text-primary font-medium{% else %}text-base-content{% endif %}">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 7h18M3 12h18M3 17h18"/>
      </svg>
      Dashboard
    </a>

    <a href="{% url 'finance:transaction-list' %}"
       class="flex items-center gap-3 px-3 py-2 rounded-lg
              hover:bg-base-200 transition-colors
              {% if 'transaction' in request.resolver_match.url_name %}bg-primary/10 text-primary font-medium{% else %}text-base-content{% endif %}">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      Transactions
    </a>

    <a href="{% url 'finance:budget-list' %}"
       class="flex items-center gap-3 px-3 py-2 rounded-lg
              hover:bg-base-200 transition-colors
              {% if 'budget' in request.resolver_match.url_name %}bg-primary/10 text-primary font-medium{% else %}text-base-content{% endif %}">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
      </svg>
      Budgets
    </a>

    <a href="{% url 'finance:account-list' %}"
       class="flex items-center gap-3 px-3 py-2 rounded-lg
              hover:bg-base-200 transition-colors
              {% if 'account' in request.resolver_match.url_name %}bg-primary/10 text-primary font-medium{% else %}text-base-content{% endif %}">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
      </svg>
      Accounts
    </a>

    <a href="{% url 'finance:reports' %}"
       class="flex items-center gap-3 px-3 py-2 rounded-lg
              hover:bg-base-200 transition-colors
              {% if 'report' in request.resolver_match.url_name %}bg-primary/10 text-primary font-medium{% else %}text-base-content{% endif %}">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
      </svg>
      Reports
    </a>
  </nav>

  {# User info #}
  <div class="p-4 border-t border-base-300">
    <div class="flex items-center gap-3">
      <div class="avatar placeholder">
        <div class="bg-neutral text-neutral-content rounded-full w-8">
          <span class="text-xs">{{ user.email|first|upper }}</span>
        </div>
      </div>
      <div class="flex-1 min-w-0">
        <p class="text-sm font-medium truncate">{{ user.get_full_name|default:user.email }}</p>
        <p class="text-xs text-base-content/50 truncate">{{ user.base_currency }}</p>
      </div>
      <a href="{% url 'accounts:profile' %}" class="btn btn-ghost btn-xs">⚙️</a>
    </div>
  </div>
</aside>
```

#### `templates/partials/_navbar.html`

```html
<header class="navbar bg-base-100 shadow-sm px-4">
  {# Breadcrumb #}
  <div class="flex-1">
    {% include "partials/_breadcrumb.html" %}
  </div>

  {# Actions #}
  <div class="flex items-center gap-2">
    {# Theme toggle #}
    <button
      class="btn btn-ghost btn-circle btn-sm"
      _="on click
         if document.documentElement.getAttribute('data-theme') == 'fintrack'
           set document.documentElement's *data-theme to 'dark'
         else
           set document.documentElement's *data-theme to 'fintrack'
         end
         localStorage.setItem('theme', document.documentElement.getAttribute('data-theme'))"
      title="Toggle theme"
    >
      🌙
    </button>

    {# Notifications #}
    <div class="dropdown dropdown-end">
      <button tabindex="0" class="btn btn-ghost btn-circle btn-sm">
        <div class="indicator">
          🔔
          {% with unread_count=request.user.notifications.filter.is_read.False.count %}
            {% if unread_count > 0 %}
              <span class="badge badge-xs badge-primary indicator-item">{{ unread_count }}</span>
            {% endif %}
          {% endwith %}
        </div>
      </button>
      <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-80">
        <li class="menu-title"><span>Notifications</span></li>
        {% for notif in request.user.notifications.all|slice:":5" %}
          <li>
            <a href="{{ notif.url }}" class="{% if not notif.is_read %}font-medium{% endif %}">
              <div>
                <p class="text-sm">{{ notif.title }}</p>
                <p class="text-xs text-base-content/50">{{ notif.created_at|timesince }} ago</p>
              </div>
            </a>
          </li>
        {% empty %}
          <li><span class="text-sm text-base-content/50">No notifications</span></li>
        {% endfor %}
        <li class="divider"></li>
        <li><a href="{% url 'notifications:list' %}">View all</a></li>
      </ul>
    </div>

    {# Logout #}
    <form method="post" action="{% url 'account_logout' %}">
      {% csrf_token %}
      <button type="submit" class="btn btn-ghost btn-sm">Logout</button>
    </form>
  </div>
</header>
```

#### `templates/partials/_breadcrumb.html`

```html
<div class="breadcrumbs text-sm">
  <ul>
    <li><a href="{% url 'finance:dashboard' %}">Home</a></li>
    {% block breadcrumb %}{% endblock %}
  </ul>
</div>
```

#### `templates/partials/_toast.html`

```html
{# Toast container kosong — diisi via OOB swap #}
```

#### `templates/partials/_pagination.html`

```html
{% if page_obj.has_other_pages %}
<div class="join mt-4 flex justify-center">
  {% if page_obj.has_previous %}
    <a
      class="join-item btn btn-sm"
      hx-get="?page={{ page_obj.previous_page_number }}&{{ request.GET.urlencode }}"
      hx-target="#transaction-list"
      hx-push-url="true"
    >«</a>
  {% else %}
    <button class="join-item btn btn-sm btn-disabled">«</button>
  {% endif %}

  {% for num in page_obj.paginator.page_range %}
    {% if num == page_obj.number %}
      <button class="join-item btn btn-sm btn-active btn-primary">{{ num }}</button>
    {% elif num > page_obj.number|add:"-3" and num < page_obj.number|add:"3" %}
      <a
        class="join-item btn btn-sm"
        hx-get="?page={{ num }}&{{ request.GET.urlencode }}"
        hx-target="#transaction-list"
        hx-push-url="true"
      >{{ num }}</a>
    {% endif %}
  {% endfor %}

  {% if page_obj.has_next %}
    <a
      class="join-item btn btn-sm"
      hx-get="?page={{ page_obj.next_page_number }}&{{ request.GET.urlencode }}"
      hx-target="#transaction-list"
      hx-push-url="true"
    >»</a>
  {% else %}
    <button class="join-item btn btn-sm btn-disabled">»</button>
  {% endif %}
</div>
{% endif %}
```

#### `templates/errors/404.html`

```html
{% extends "base.html" %}
{% block title %}404 Not Found — FinTrack{% endblock %}
{% block content %}
<div class="hero min-h-96">
  <div class="hero-content text-center">
    <div>
      <h1 class="text-8xl font-bold text-primary">404</h1>
      <p class="text-2xl mt-4">Page not found</p>
      <p class="text-base-content/60 mt-2">The page you're looking for doesn't exist.</p>
      <a href="{% url 'finance:dashboard' %}" class="btn btn-primary mt-6">Go Home</a>
    </div>
  </div>
</div>
{% endblock %}
```

#### `templates/errors/500.html`

```html
{% extends "base.html" %}
{% block title %}500 Server Error — FinTrack{% endblock %}
{% block content %}
<div class="hero min-h-96">
  <div class="hero-content text-center">
    <div>
      <h1 class="text-8xl font-bold text-error">500</h1>
      <p class="text-2xl mt-4">Something went wrong</p>
      <p class="text-base-content/60 mt-2">We're working on fixing this.</p>
      <a href="{% url 'finance:dashboard' %}" class="btn btn-primary mt-6">Go Home</a>
    </div>
  </div>
</div>
{% endblock %}
```

---

### 4.3 Custom Template Tags

#### `apps/core/templatetags/finance_tags.py`

```python
from django import template
from django.utils.formats import number_format

register = template.Library()


@register.filter
def currency(value, currency_code="IDR"):
    """Format angka sebagai currency. Contoh: {{ amount|currency:'IDR' }}"""
    try:
        value = float(value)
        formatted = number_format(value, decimal_pos=0, use_l10n=True)
        currency_symbols = {
            "IDR": "Rp",
            "USD": "$",
            "EUR": "€",
            "SGD": "S$",
            "JPY": "¥",
        }
        symbol = currency_symbols.get(currency_code, currency_code)
        return f"{symbol} {formatted}"
    except (ValueError, TypeError):
        return value


@register.filter
def percentage(value, decimals=1):
    """Format sebagai persentase. Contoh: {{ ratio|percentage }}"""
    try:
        return f"{float(value):.{decimals}f}%"
    except (ValueError, TypeError):
        return "0%"


@register.filter
def abs_value(value):
    """Nilai absolut."""
    try:
        return abs(value)
    except (ValueError, TypeError):
        return value


@register.simple_tag
def budget_progress_color(percentage):
    """Return DaisyUI progress color berdasarkan persentase."""
    if percentage >= 100:
        return "progress-error"
    elif percentage >= 80:
        return "progress-warning"
    elif percentage >= 50:
        return "progress-info"
    return "progress-success"
```

#### `apps/core/templatetags/htmx_tags.py`

```python
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def htmx_or_full(context, htmx_template, full_template):
    """
    Pilih template berdasarkan apakah request adalah HTMX.
    Penggunaan: {% htmx_or_full 'partial.html' 'full.html' %}
    """
    request = context.get("request")
    if request and getattr(request, "htmx", None):
        return htmx_template
    return full_template
```

---

### 4.4 Context Processors

Sudah ada di `apps/core/context_processors.py` (lihat bagian 2.1).

---

## FASE 5 — Authentication (django-allauth)

### 5.1 Konfigurasi Allauth

Allauth sudah dikonfigurasi di `base.py`. Tambahkan template override:

#### `apps/accounts/templates/accounts/login.html`

```html
{% extends "base.html" %}
{% load widget_tweaks %}

{% block title %}Login — FinTrack{% endblock %}

{% block auth_content %}
<div class="card w-full max-w-md bg-base-100 shadow-xl">
  <div class="card-body">
    <div class="text-center mb-6">
      <div class="w-12 h-12 bg-primary rounded-xl flex items-center justify-center mx-auto mb-3">
        <span class="text-white font-bold text-lg">FT</span>
      </div>
      <h1 class="text-2xl font-bold">Welcome back</h1>
      <p class="text-base-content/60 text-sm">Sign in to your FinTrack account</p>
    </div>

    <form method="post" action="{% url 'account_login' %}">
      {% csrf_token %}

      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text font-medium">Email</span>
        </label>
        {{ form.login|add_class:"input input-bordered w-full" }}
        {% if form.login.errors %}
          <label class="label">
            <span class="label-text-alt text-error">{{ form.login.errors|first }}</span>
          </label>
        {% endif %}
      </div>

      <div class="form-control mb-6">
        <label class="label">
          <span class="label-text font-medium">Password</span>
          <a href="{% url 'account_reset_password' %}" class="label-text-alt link link-primary">
            Forgot password?
          </a>
        </label>
        {{ form.password|add_class:"input input-bordered w-full" }}
        {% if form.password.errors %}
          <label class="label">
            <span class="label-text-alt text-error">{{ form.password.errors|first }}</span>
          </label>
        {% endif %}
      </div>

      <button type="submit" class="btn btn-primary w-full">Sign In</button>
    </form>

    <div class="divider text-base-content/40">or</div>

    <a href="{% url 'socialaccount_signup' %}?next=/" class="btn btn-outline w-full gap-2">
      <svg class="w-5 h-5" viewBox="0 0 24 24">
        <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
        <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
        <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
        <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
      </svg>
      Continue with Google
    </a>

    <p class="text-center text-sm text-base-content/60 mt-4">
      Don't have an account?
      <a href="{% url 'account_signup' %}" class="link link-primary">Sign up</a>
    </p>
  </div>
</div>
{% endblock %}
```

Buat `allauth` menggunakan template kita dengan override. Tambahkan ke settings:

```python
# base.py — tambahkan
ACCOUNT_FORMS = {
    "login": "allauth.account.forms.LoginForm",
}
# Atau arahkan template allauth ke folder kita:
# templates/account/login.html akan otomatis dipakai allauth
```

**Buat folder dan salin template allauth:**

```bash
mkdir -p templates/account
# Allauth akan mencari templates/account/login.html, signup.html, dll.
```

---

### 5.2 Custom Auth Templates

Buat `templates/account/login.html` (allauth memakai folder `account/`):

```bash
# Salin dari apps/accounts/templates ke templates/account/
# Atau buat langsung:
touch templates/account/login.html
touch templates/account/signup.html
touch templates/account/password_reset.html
touch templates/account/email_confirm.html
```

Isi `templates/account/signup.html` dengan struktur yang mirip login tetapi dengan field yang sesuai.

---

### 5.3 Profile & Team Views

Sudah didefinisikan di `apps/accounts/views.py` (lihat bagian 2.2).

#### `apps/accounts/templates/accounts/profile.html`

```html
{% extends "base.html" %}
{% load widget_tweaks %}

{% block title %}Profile — FinTrack{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto space-y-6">
  <div>
    <h1 class="text-2xl font-bold">Profile Settings</h1>
    <p class="text-base-content/60 text-sm">Update your personal information</p>
  </div>

  <div class="card bg-base-100 shadow-sm">
    <div class="card-body">
      <form method="post" enctype="multipart/form-data">
        {% csrf_token %}

        <div class="form-control mb-4">
          <label class="label"><span class="label-text font-medium">Full Name</span></label>
          <div class="grid grid-cols-2 gap-3">
            {{ form.first_name|add_class:"input input-bordered w-full" }}
            {{ form.last_name|add_class:"input input-bordered w-full" }}
          </div>
        </div>

        <div class="form-control mb-4">
          <label class="label"><span class="label-text font-medium">Base Currency</span></label>
          {{ form.base_currency|add_class:"select select-bordered w-full" }}
        </div>

        <div class="form-control mb-4">
          <label class="label"><span class="label-text font-medium">Timezone</span></label>
          {{ form.timezone|add_class:"select select-bordered w-full" }}
        </div>

        <div class="card-actions justify-end mt-4">
          <button type="submit" class="btn btn-primary">Save Changes</button>
        </div>
      </form>
    </div>
  </div>
</div>
{% endblock %}
```

---

## FASE 6 — Core Mixins & Middleware

### 6.1 View Mixins (HtmxMixin, OwnershipMixin)

#### `apps/core/mixins.py`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django_htmx.http import HttpResponseClientRedirect


class HtmxMixin:
    """
    Mixin untuk view yang merespons baik HTMX maupun regular request.
    Tentukan htmx_template untuk partial response.
    """
    htmx_template: str = ""
    full_template: str = ""

    def get_template_names(self):
        if getattr(self.request, "htmx", None) and self.htmx_template:
            return [self.htmx_template]
        if self.full_template:
            return [self.full_template]
        return super().get_template_names()

    def htmx_redirect(self, url: str):
        """Redirect yang benar di dalam HTMX request."""
        if getattr(self.request, "htmx", None):
            return HttpResponseClientRedirect(url)
        from django.shortcuts import redirect
        return redirect(url)


class OwnershipMixin:
    """Pastikan user hanya bisa akses object miliknya sendiri."""
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class FinanceViewMixin(LoginRequiredMixin, OwnershipMixin, HtmxMixin):
    """Base mixin untuk semua finance views."""
    pass


class HtmxOnlyMixin:
    """Tolak request yang bukan dari HTMX."""
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request, "htmx", None):
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest("This endpoint is HTMX-only.")
        return super().dispatch(request, *args, **kwargs)
```

---

### 6.2 Custom Middleware

#### `apps/core/middleware.py`

```python
import zoneinfo
from django.utils import timezone


class TimezoneMiddleware:
    """Aktifkan timezone berdasarkan preference user."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_tz = getattr(request.user, "timezone", "UTC")
            try:
                tzinfo = zoneinfo.ZoneInfo(user_tz)
                timezone.activate(tzinfo)
            except Exception:
                timezone.deactivate()
        else:
            timezone.deactivate()
        return self.get_response(request)


_current_user_storage = {}


class CurrentUserMiddleware:
    """Simpan current user di thread-local storage untuk akses di signals/services."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import threading
        _current_user_storage[threading.get_ident()] = (
            request.user if request.user.is_authenticated else None
        )
        response = self.get_response(request)
        _current_user_storage.pop(threading.get_ident(), None)
        return response


def get_current_user():
    """Dapatkan user yang sedang login dari mana saja."""
    import threading
    return _current_user_storage.get(threading.get_ident())


class HtmxSecurityMiddleware:
    """Pastikan HTMX request berasal dari host yang sama."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, "htmx", None):
            current_url = request.META.get("HTTP_HX_CURRENT_URL", "")
            if current_url:
                from django.conf import settings
                allowed = f"{request.scheme}://{request.get_host()}"
                if not current_url.startswith(allowed):
                    from django.http import HttpResponseForbidden
                    return HttpResponseForbidden("Invalid HTMX origin")
        return self.get_response(request)
```

---

### 6.3 Permissions Helpers

#### `apps/core/permissions.py`

```python
from django.core.exceptions import PermissionDenied


def assert_owns(user, obj) -> None:
    """
    Raise PermissionDenied jika user tidak memiliki object.
    Supports user FK dan team membership.
    """
    if hasattr(obj, "user") and obj.user_id != user.pk:
        raise PermissionDenied(
            f"User {user.email} does not own {obj.__class__.__name__} {obj.pk}"
        )
    if hasattr(obj, "team") and obj.team:
        if not obj.team.memberships.filter(user=user).exists():
            raise PermissionDenied(
                f"User {user.email} is not a member of team {obj.team.name}"
            )
```

---

## FASE 7 — Service Layer & Repository

### 7.1 Transaction Service

#### `apps/finance/services/transaction_service.py`

```python
from decimal import Decimal
from typing import Optional
from datetime import date

from django.db import transaction as db_transaction
from django.contrib.auth import get_user_model

from apps.finance.models import Transaction, FinancialAccount, Category, RecurringTransaction
from apps.finance.repositories.transaction_repo import TransactionRepository

User = get_user_model()


class TransactionService:
    def __init__(self, repo: Optional[TransactionRepository] = None):
        self.repo = repo or TransactionRepository()

    @db_transaction.atomic
    def create_transaction(
        self,
        user: User,
        account: FinancialAccount,
        category: Optional[Category],
        transaction_type: str,
        amount: Decimal,
        date: date,
        description: str,
        **kwargs,
    ) -> Transaction:
        """Buat transaksi baru dan update saldo akun."""
        txn = self.repo.create(
            user=user,
            account=account,
            category=category,
            transaction_type=transaction_type,
            amount=amount,
            currency=account.currency,
            date=date,
            description=description,
            **kwargs,
        )
        self._update_account_balance(account, txn)
        self._check_budget_alerts(user, txn)
        return txn

    @db_transaction.atomic
    def update_transaction(self, txn: Transaction, **fields) -> Transaction:
        """Update transaksi, balik dulu dampak saldo lama."""
        old_amount = txn.amount
        old_type = txn.transaction_type
        old_account = txn.account

        updated = self.repo.update(txn, **fields)

        # Balik dampak lama
        self._reverse_account_balance(old_account, old_amount, old_type)
        # Terapkan dampak baru
        self._update_account_balance(updated.account, updated)
        return updated

    @db_transaction.atomic
    def delete_transaction(self, txn: Transaction) -> None:
        """Soft-delete dan balik saldo akun."""
        self._reverse_account_balance(txn.account, txn.amount, txn.transaction_type)
        txn.delete()

    @db_transaction.atomic
    def create_from_recurring(
        self, recurring: RecurringTransaction, date: date
    ) -> Transaction:
        """Buat transaksi dari template recurring."""
        return self.create_transaction(
            user=recurring.user,
            account=recurring.account,
            category=recurring.category,
            transaction_type=recurring.transaction_type,
            amount=recurring.amount,
            date=date,
            description=recurring.description,
            is_recurring_instance=True,
            recurring_transaction=recurring,
        )

    def _update_account_balance(
        self, account: FinancialAccount, txn: Transaction
    ) -> None:
        if txn.transaction_type == Transaction.TYPE_INCOME:
            account.current_balance += txn.amount
        elif txn.transaction_type == Transaction.TYPE_EXPENSE:
            account.current_balance -= txn.amount
        elif txn.transaction_type == Transaction.TYPE_TRANSFER and txn.transfer_to_account:
            account.current_balance -= txn.amount
            txn.transfer_to_account.current_balance += txn.amount
            txn.transfer_to_account.save(update_fields=["current_balance"])
        account.save(update_fields=["current_balance"])

    def _reverse_account_balance(
        self, account: FinancialAccount, amount: Decimal, txn_type: str
    ) -> None:
        if txn_type == Transaction.TYPE_INCOME:
            account.current_balance -= amount
        elif txn_type == Transaction.TYPE_EXPENSE:
            account.current_balance += amount
        account.save(update_fields=["current_balance"])

    def _check_budget_alerts(self, user: User, txn: Transaction) -> None:
        if txn.transaction_type != Transaction.TYPE_EXPENSE or not txn.category:
            return
        from apps.finance.services.budget_service import BudgetService
        BudgetService().check_and_alert(user, txn.category)
```

---

### 7.2 Budget Service

#### `apps/finance/services/budget_service.py`

```python
from decimal import Decimal
from datetime import date
from typing import Optional

from django.db.models import Sum, Q
from django.contrib.auth import get_user_model

from apps.finance.models import Budget, Category, Transaction

User = get_user_model()


class BudgetService:
    def get_active_budgets_with_usage(self, user: User, ref_date: Optional[date] = None):
        """
        Kembalikan budget aktif beserta jumlah yang sudah dipakai.
        """
        ref_date = ref_date or date.today()
        budgets = Budget.objects.filter(
            user=user, is_active=True
        ).select_related("category")

        result = []
        for budget in budgets:
            spent = self._get_spent_amount(user, budget, ref_date)
            percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0
            result.append({
                "budget": budget,
                "spent": spent,
                "remaining": max(budget.amount - spent, Decimal("0")),
                "percentage": round(percentage, 1),
                "is_over": spent > budget.amount,
            })
        return result

    def _get_spent_amount(
        self, user: User, budget: Budget, ref_date: date
    ) -> Decimal:
        """Hitung total pengeluaran untuk budget di periode aktif."""
        from apps.finance.utils.dates import get_period_dates
        start, end = get_period_dates(budget.period, ref_date)

        result = Transaction.objects.filter(
            user=user,
            category=budget.category,
            transaction_type=Transaction.TYPE_EXPENSE,
            date__gte=start,
            date__lte=end,
        ).aggregate(total=Sum("amount"))
        return result["total"] or Decimal("0")

    def check_and_alert(self, user: User, category: Category) -> None:
        """Cek apakah budget melebihi threshold dan kirim alert."""
        budgets = Budget.objects.filter(
            user=user, category=category, is_active=True, alert_sent=False
        )
        for budget in budgets:
            usage = self.get_active_budgets_with_usage(user)
            for item in usage:
                if item["budget"].pk == budget.pk:
                    if item["percentage"] >= budget.alert_at_percentage:
                        self._send_budget_alert(budget, item["percentage"])
                    break

    def _send_budget_alert(self, budget: Budget, percentage: float) -> None:
        from apps.finance.tasks import send_budget_alert
        send_budget_alert.delay(str(budget.pk), budget.user_id, percentage)
        budget.alert_sent = True
        budget.save(update_fields=["alert_sent"])
```

---

### 7.3 Report Service

#### `apps/finance/services/report_service.py`

```python
from decimal import Decimal
from datetime import date
from typing import Optional

from django.db.models import Sum, Q, Count
from django.contrib.auth import get_user_model

from apps.finance.models import Transaction, Category

User = get_user_model()


class ReportService:
    def get_summary(
        self,
        user: User,
        start_date: date,
        end_date: date,
    ) -> dict:
        """Summary: total income, expense, net, dan per-category."""
        qs = Transaction.objects.filter(
            user=user, date__gte=start_date, date__lte=end_date
        )

        totals = qs.aggregate(
            total_income=Sum("amount", filter=Q(transaction_type="income")),
            total_expense=Sum("amount", filter=Q(transaction_type="expense")),
        )
        total_income = totals["total_income"] or Decimal("0")
        total_expense = totals["total_expense"] or Decimal("0")

        by_category = (
            qs.filter(transaction_type="expense")
            .values("category__name", "category__color", "category__icon")
            .annotate(total=Sum("amount"), count=Count("id"))
            .order_by("-total")
        )

        monthly_trend = []
        from apps.finance.utils.dates import months_between
        for year, month in months_between(start_date, end_date):
            month_qs = qs.filter(date__year=year, date__month=month)
            month_totals = month_qs.aggregate(
                income=Sum("amount", filter=Q(transaction_type="income")),
                expense=Sum("amount", filter=Q(transaction_type="expense")),
            )
            monthly_trend.append({
                "year": year,
                "month": month,
                "income": month_totals["income"] or 0,
                "expense": month_totals["expense"] or 0,
            })

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net": total_income - total_expense,
            "by_category": list(by_category),
            "monthly_trend": monthly_trend,
        }
```

---

### 7.4 Import Service (CSV)

#### `apps/finance/services/import_service.py`

```python
import csv
import io
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Generator

from django.contrib.auth import get_user_model

User = get_user_model()

REQUIRED_COLUMNS = {"date", "description", "amount", "type"}


class ImportError(Exception):
    pass


class TransactionImportService:
    def parse_csv(self, file_content: str) -> Generator[dict, None, None]:
        """Parse CSV dan yield setiap baris sebagai dict."""
        reader = csv.DictReader(io.StringIO(file_content))

        # Validasi kolom
        if not reader.fieldnames:
            raise ImportError("CSV file is empty")

        missing = REQUIRED_COLUMNS - set(
            col.strip().lower() for col in reader.fieldnames
        )
        if missing:
            raise ImportError(f"Missing required columns: {', '.join(missing)}")

        for i, row in enumerate(reader, start=2):
            try:
                yield self._parse_row(row, line=i)
            except (ValueError, InvalidOperation) as e:
                raise ImportError(f"Error on line {i}: {e}")

    def _parse_row(self, row: dict, line: int) -> dict:
        row = {k.strip().lower(): v.strip() for k, v in row.items()}

        # Parse date
        date_str = row.get("date", "")
        for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]:
            try:
                parsed_date = datetime.strptime(date_str, fmt).date()
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"Invalid date format: {date_str}")

        # Parse amount
        amount_str = row.get("amount", "0").replace(",", "").replace(" ", "")
        amount = Decimal(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Parse type
        txn_type = row.get("type", "").lower()
        if txn_type not in ("income", "expense"):
            raise ValueError(f"Invalid type: {txn_type}. Must be 'income' or 'expense'")

        return {
            "date": parsed_date,
            "description": row.get("description", ""),
            "amount": amount,
            "transaction_type": txn_type,
            "payee": row.get("payee", ""),
            "notes": row.get("notes", ""),
            "category_name": row.get("category", ""),
        }
```

---

### 7.5 Currency Service

#### `apps/finance/services/currency_service.py`

```python
import logging
from decimal import Decimal
from typing import Optional

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_KEY = "fintrack:exchange_rates"
CACHE_TTL = settings.FINTRACK_EXCHANGE_RATE_REFRESH_HOURS * 3600


class CurrencyService:
    def get_rate(self, from_currency: str, to_currency: str) -> Optional[Decimal]:
        """Ambil rate konversi (melalui cache)."""
        if from_currency == to_currency:
            return Decimal("1")

        rates = self._get_all_rates()
        if not rates:
            return None

        # Konversi melalui base currency (USD)
        try:
            from_to_usd = Decimal(str(rates.get(from_currency, 1)))
            to_from_usd = Decimal(str(rates.get(to_currency, 1)))
            return to_from_usd / from_to_usd
        except Exception:
            return None

    def convert(
        self, amount: Decimal, from_currency: str, to_currency: str
    ) -> Optional[Decimal]:
        rate = self.get_rate(from_currency, to_currency)
        if rate is None:
            return None
        return amount * rate

    def refresh_all_rates(self) -> None:
        """Refresh rates dari API eksternal dan simpan ke cache."""
        api_key = getattr(settings, "EXCHANGERATE_API_KEY", "")
        if not api_key:
            logger.warning("EXCHANGERATE_API_KEY not set, skipping refresh")
            return

        try:
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            rates = data.get("conversion_rates", {})
            cache.set(CACHE_KEY, rates, CACHE_TTL)
            logger.info("Exchange rates refreshed successfully")
        except Exception as e:
            logger.error(f"Failed to refresh exchange rates: {e}")

    def _get_all_rates(self) -> Optional[dict]:
        return cache.get(CACHE_KEY)
```

#### `apps/finance/utils/dates.py`

```python
from datetime import date
from typing import Generator, Tuple


def get_period_dates(period: str, ref_date: date) -> Tuple[date, date]:
    """Return (start, end) untuk period tertentu."""
    from dateutil.relativedelta import relativedelta

    if period == "weekly":
        start = ref_date - relativedelta(days=ref_date.weekday())
        end = start + relativedelta(days=6)
    elif period == "monthly":
        start = ref_date.replace(day=1)
        end = (start + relativedelta(months=1)) - relativedelta(days=1)
    elif period == "quarterly":
        quarter = (ref_date.month - 1) // 3
        start = date(ref_date.year, quarter * 3 + 1, 1)
        end = (start + relativedelta(months=3)) - relativedelta(days=1)
    elif period == "yearly":
        start = date(ref_date.year, 1, 1)
        end = date(ref_date.year, 12, 31)
    else:
        # Custom or default: current month
        start = ref_date.replace(day=1)
        end = (start + relativedelta(months=1)) - relativedelta(days=1)

    return start, end


def months_between(start: date, end: date) -> Generator[Tuple[int, int], None, None]:
    """Yield (year, month) untuk setiap bulan antara start dan end."""
    current = start.replace(day=1)
    while current <= end:
        yield current.year, current.month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
```

#### `apps/finance/utils/currency.py`

```python
from decimal import Decimal


CURRENCY_SYMBOLS = {
    "IDR": "Rp",
    "USD": "$",
    "EUR": "€",
    "SGD": "S$",
    "JPY": "¥",
    "GBP": "£",
}


def format_currency(amount: Decimal, currency: str) -> str:
    symbol = CURRENCY_SYMBOLS.get(currency, currency)
    if currency in ("IDR", "JPY"):
        return f"{symbol} {amount:,.0f}"
    return f"{symbol} {amount:,.2f}"
```

---

### 7.6 Transaction Repository

#### `apps/finance/repositories/transaction_repo.py`

```python
from typing import Optional
from decimal import Decimal
from datetime import date

from django.db.models import QuerySet, Sum, Q

from apps.finance.models import Transaction


class TransactionRepository:
    """Enkapsulasi semua DB query untuk model Transaction."""

    def get_user_transactions(
        self,
        user,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category_id: Optional[str] = None,
        account_id: Optional[str] = None,
        transaction_type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> QuerySet:
        qs = (
            Transaction.objects
            .filter(user=user)
            .select_related("account", "category")
            .prefetch_related("tags")
        )
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        if category_id:
            qs = qs.filter(category_id=category_id)
        if account_id:
            qs = qs.filter(account_id=account_id)
        if transaction_type:
            qs = qs.filter(transaction_type=transaction_type)
        if search:
            qs = qs.filter(
                Q(description__icontains=search)
                | Q(payee__icontains=search)
                | Q(notes__icontains=search)
            )
        return qs

    def get_monthly_summary(self, user, year: int, month: int) -> dict:
        qs = Transaction.objects.filter(
            user=user, date__year=year, date__month=month
        )
        result = qs.aggregate(
            total_income=Sum("amount", filter=Q(transaction_type="income")),
            total_expense=Sum("amount", filter=Q(transaction_type="expense")),
        )
        result["total_income"] = result["total_income"] or Decimal("0")
        result["total_expense"] = result["total_expense"] or Decimal("0")
        result["net"] = result["total_income"] - result["total_expense"]
        return result

    def get_recent(self, user, limit: int = 10) -> QuerySet:
        return (
            Transaction.objects
            .filter(user=user)
            .select_related("account", "category")
            .order_by("-date", "-created_at")[:limit]
        )

    def create(self, **kwargs) -> Transaction:
        return Transaction.objects.create(**kwargs)

    def update(self, txn: Transaction, **fields) -> Transaction:
        for attr, value in fields.items():
            setattr(txn, attr, value)
        txn.save()
        return txn
```

---

### 7.7 Budget Repository

#### `apps/finance/repositories/budget_repo.py`

```python
from typing import Optional
from datetime import date

from django.db.models import QuerySet

from apps.finance.models import Budget


class BudgetRepository:
    def get_active_budgets(self, user, ref_date: Optional[date] = None) -> QuerySet:
        qs = Budget.objects.filter(
            user=user, is_active=True
        ).select_related("category")

        if ref_date:
            qs = qs.filter(
                Q(end_date__isnull=True) | Q(end_date__gte=ref_date),
                start_date__lte=ref_date,
            )
        return qs

    def create(self, **kwargs) -> Budget:
        return Budget.objects.create(**kwargs)

    def update(self, budget: Budget, **fields) -> Budget:
        for attr, value in fields.items():
            setattr(budget, attr, value)
        budget.save()
        return budget
```

---

## FASE 8 — Forms

### 8.1 Transaction Form

#### `apps/finance/forms/transaction_form.py`

```python
from django import forms
from django.db.models import Q
from apps.finance.models import Transaction, FinancialAccount, Category, Tag


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "transaction_type", "account", "category",
            "amount", "date", "description", "payee",
            "notes", "tags", "status", "reference_number",
        ]
        widgets = {
            "transaction_type": forms.Select(
                attrs={"class": "select select-bordered w-full",
                       "hx-get": "", "hx-target": "#category-field",
                       "hx-trigger": "change"}
            ),
            "account": forms.Select(
                attrs={"class": "select select-bordered w-full"}
            ),
            "category": forms.Select(
                attrs={"class": "select select-bordered w-full", "id": "id_category"}
            ),
            "amount": forms.NumberInput(attrs={
                "class": "input input-bordered w-full",
                "step": "0.01", "min": "0.01",
                "placeholder": "0.00",
            }),
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "input input-bordered w-full",
            }),
            "description": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "What was this for?",
            }),
            "payee": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Merchant or person",
            }),
            "notes": forms.Textarea(attrs={
                "class": "textarea textarea-bordered w-full",
                "rows": 2,
                "placeholder": "Optional notes...",
            }),
            "status": forms.Select(
                attrs={"class": "select select-bordered w-full"}
            ),
            "reference_number": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Optional reference",
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["account"].queryset = FinancialAccount.objects.filter(
                user=user, is_active=True
            )
            self.fields["category"].queryset = Category.objects.filter(
                Q(user=user) | Q(is_system=True)
            )
            self.fields["tags"].queryset = Tag.objects.filter(user=user)

        # Set tanggal default hari ini
        if not self.instance.pk:
            from django.utils import timezone
            self.fields["date"].initial = timezone.localdate()

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned = super().clean()
        txn_type = cleaned.get("transaction_type")
        category = cleaned.get("category")

        if category and txn_type:
            if (category.category_type != txn_type
                    and category.category_type != "transfer"):
                self.add_error(
                    "category",
                    f"Category type '{category.category_type}' doesn't match "
                    f"transaction type '{txn_type}'."
                )
        return cleaned
```

#### `apps/finance/forms/__init__.py`

```python
from .transaction_form import TransactionForm
from .budget_form import BudgetForm
from .account_form import AccountForm
from .import_form import ImportForm

__all__ = ["TransactionForm", "BudgetForm", "AccountForm", "ImportForm"]
```

---

### 8.2 Budget Form

#### `apps/finance/forms/budget_form.py`

```python
from django import forms
from django.db.models import Q
from apps.finance.models import Budget, Category


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = [
            "name", "category", "amount", "currency",
            "period", "start_date", "end_date",
            "alert_at_percentage",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "category": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "amount": forms.NumberInput(attrs={
                "class": "input input-bordered w-full",
                "step": "0.01", "min": "0.01",
            }),
            "currency": forms.Select(
                attrs={"class": "select select-bordered w-full"},
                choices=[
                    ("IDR", "IDR"), ("USD", "USD"), ("EUR", "EUR"),
                    ("SGD", "SGD"), ("JPY", "JPY"),
                ],
            ),
            "period": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "start_date": forms.DateInput(attrs={
                "type": "date", "class": "input input-bordered w-full"
            }),
            "end_date": forms.DateInput(attrs={
                "type": "date", "class": "input input-bordered w-full"
            }),
            "alert_at_percentage": forms.NumberInput(attrs={
                "class": "input input-bordered w-full",
                "min": "1", "max": "100",
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["category"].queryset = Category.objects.filter(
                Q(user=user) | Q(is_system=True),
                category_type="expense",
            )
```

---

### 8.3 Account Form

#### `apps/finance/forms/account_form.py`

```python
from django import forms
from apps.finance.models import FinancialAccount


class AccountForm(forms.ModelForm):
    class Meta:
        model = FinancialAccount
        fields = [
            "name", "account_type", "currency",
            "initial_balance", "color", "icon",
            "institution_name", "last_four_digits", "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "e.g. BCA Main Account",
            }),
            "account_type": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "currency": forms.Select(
                attrs={"class": "select select-bordered w-full"},
                choices=[
                    ("IDR", "IDR — Rupiah"), ("USD", "USD — Dollar"),
                    ("EUR", "EUR — Euro"), ("SGD", "SGD — SGD"),
                    ("JPY", "JPY — Yen"),
                ],
            ),
            "initial_balance": forms.NumberInput(attrs={
                "class": "input input-bordered w-full",
                "step": "0.01", "min": "0",
            }),
            "color": forms.TextInput(attrs={
                "type": "color", "class": "input input-bordered w-full h-10",
            }),
            "icon": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "wallet, bank, card, ...",
            }),
            "institution_name": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "e.g. Bank BCA",
            }),
            "last_four_digits": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "maxlength": "4", "placeholder": "Last 4 digits",
            }),
            "notes": forms.Textarea(attrs={
                "class": "textarea textarea-bordered w-full", "rows": 2,
            }),
        }
```

---

### 8.4 Import Form (CSV)

#### `apps/finance/forms/import_form.py`

```python
from django import forms


class ImportForm(forms.Form):
    csv_file = forms.FileField(
        label="CSV File",
        help_text="Upload a CSV file with columns: date, description, amount, type, [payee, notes, category]",
        widget=forms.FileInput(attrs={"class": "file-input file-input-bordered w-full", "accept": ".csv"}),
    )
    account = forms.ChoiceField(
        label="Target Account",
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )
    skip_duplicates = forms.BooleanField(
        label="Skip duplicate transactions",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            from apps.finance.models import FinancialAccount
            accounts = FinancialAccount.objects.filter(user=user, is_active=True)
            self.fields["account"].choices = [
                (str(a.pk), f"{a.name} ({a.currency})")
                for a in accounts
            ]
```

---

## FASE 9 — Views & URL Routing

### 9.1 Finance URL Config

#### `apps/finance/urls.py`

```python
from django.urls import path
from apps.finance.views import dashboard, transactions, budgets, accounts, reports

app_name = "finance"

urlpatterns = [
    # ── Dashboard ─────────────────────────────────────────────
    path("dashboard/", dashboard.DashboardView.as_view(), name="dashboard"),
    path("dashboard/summary/", dashboard.DashboardSummaryView.as_view(), name="dashboard-summary"),

    # ── Transactions ──────────────────────────────────────────
    path("transactions/", transactions.TransactionListView.as_view(), name="transaction-list"),
    path("transactions/create/", transactions.TransactionCreateView.as_view(), name="transaction-create"),
    path("transactions/<uuid:pk>/", transactions.TransactionDetailView.as_view(), name="transaction-detail"),
    path("transactions/<uuid:pk>/edit/", transactions.TransactionUpdateView.as_view(), name="transaction-update"),
    path("transactions/<uuid:pk>/delete/", transactions.TransactionDeleteView.as_view(), name="transaction-delete"),
    path("transactions/import/", transactions.TransactionImportView.as_view(), name="transaction-import"),
    path("transactions/export/", transactions.TransactionExportView.as_view(), name="transaction-export"),
    # HTMX-only partials
    path("transactions/filter/", transactions.TransactionFilterView.as_view(), name="transaction-filter"),
    path("transactions/<uuid:pk>/row/", transactions.TransactionRowView.as_view(), name="transaction-row"),

    # ── Budgets ───────────────────────────────────────────────
    path("budgets/", budgets.BudgetListView.as_view(), name="budget-list"),
    path("budgets/create/", budgets.BudgetCreateView.as_view(), name="budget-create"),
    path("budgets/<uuid:pk>/edit/", budgets.BudgetUpdateView.as_view(), name="budget-update"),
    path("budgets/<uuid:pk>/delete/", budgets.BudgetDeleteView.as_view(), name="budget-delete"),
    path("budgets/<uuid:pk>/row/", budgets.BudgetRowView.as_view(), name="budget-row"),

    # ── Accounts ──────────────────────────────────────────────
    path("accounts-list/", accounts.AccountListView.as_view(), name="account-list"),
    path("accounts/create/", accounts.AccountCreateView.as_view(), name="account-create"),
    path("accounts/<uuid:pk>/", accounts.AccountDetailView.as_view(), name="account-detail"),
    path("accounts/<uuid:pk>/edit/", accounts.AccountUpdateView.as_view(), name="account-update"),

    # ── Reports ───────────────────────────────────────────────
    path("reports/", reports.ReportView.as_view(), name="reports"),
    path("reports/data/", reports.ReportDataView.as_view(), name="reports-data"),
    path("reports/export/csv/", reports.ReportExportCsvView.as_view(), name="reports-export-csv"),
]
```

---

### 9.2 Dashboard Views

#### `apps/finance/views/dashboard.py`

```python
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone

from apps.core.mixins import HtmxMixin
from apps.finance.repositories.transaction_repo import TransactionRepository
from apps.finance.services.budget_service import BudgetService


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "finance/dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()
        repo = TransactionRepository()

        ctx["summary"] = repo.get_monthly_summary(
            self.request.user, today.year, today.month
        )
        ctx["recent_transactions"] = repo.get_recent(self.request.user, limit=10)
        ctx["budgets"] = BudgetService().get_active_budgets_with_usage(
            self.request.user, ref_date=today
        )
        ctx["today"] = today
        return ctx


class DashboardSummaryView(LoginRequiredMixin, HtmxMixin, TemplateView):
    """HTMX polling endpoint untuk KPI cards."""
    template_name = "finance/dashboard/_kpi_cards.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()
        repo = TransactionRepository()
        ctx["summary"] = repo.get_monthly_summary(
            self.request.user, today.year, today.month
        )
        ctx["today"] = today
        return ctx
```

---

### 9.3 Transaction Views

#### `apps/finance/views/transactions.py`

```python
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django_htmx.http import trigger_client_event, HttpResponseClientRefresh

from apps.core.mixins import FinanceViewMixin, HtmxOnlyMixin
from apps.finance.models import Transaction
from apps.finance.forms import TransactionForm, ImportForm
from apps.finance.services.transaction_service import TransactionService
from apps.finance.services.import_service import TransactionImportService, ImportError
from apps.finance.repositories.transaction_repo import TransactionRepository


class TransactionListView(FinanceViewMixin, ListView):
    model = Transaction
    full_template = "finance/transactions/list.html"
    htmx_template = "finance/transactions/_list_partial.html"
    context_object_name = "transactions"
    paginate_by = 25

    def get_template_names(self):
        return super().get_template_names()

    def get_queryset(self):
        repo = TransactionRepository()
        return repo.get_user_transactions(
            user=self.request.user,
            start_date=self.request.GET.get("start_date") or None,
            end_date=self.request.GET.get("end_date") or None,
            category_id=self.request.GET.get("category") or None,
            account_id=self.request.GET.get("account") or None,
            transaction_type=self.request.GET.get("type") or None,
            search=self.request.GET.get("q") or None,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filters"] = self.request.GET
        return ctx


class TransactionCreateView(FinanceViewMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    full_template = "finance/transactions/list.html"
    htmx_template = "finance/transactions/_form.html"
    success_url = reverse_lazy("finance:transaction-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        service = TransactionService()
        data = form.cleaned_data
        extra = {
            k: v for k, v in data.items()
            if k not in ("account", "category", "transaction_type",
                         "amount", "date", "description")
        }
        service.create_transaction(
            user=self.request.user,
            account=data["account"],
            category=data.get("category"),
            transaction_type=data["transaction_type"],
            amount=data["amount"],
            date=data["date"],
            description=data["description"],
            **extra,
        )
        messages.success(self.request, "Transaction added successfully.")

        if getattr(self.request, "htmx", None):
            response = HttpResponse(status=204)
            trigger_client_event(response, "transactionAdded", {})
            return response
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        if getattr(self.request, "htmx", None):
            return self.render_to_response(
                self.get_context_data(form=form), status=422
            )
        return super().form_invalid(form)


class TransactionDetailView(FinanceViewMixin, DetailView):
    model = Transaction
    template_name = "finance/transactions/detail.html"


class TransactionUpdateView(FinanceViewMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    full_template = "finance/transactions/list.html"
    htmx_template = "finance/transactions/_form.html"
    success_url = reverse_lazy("finance:transaction-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        service = TransactionService()
        service.update_transaction(self.object, **form.cleaned_data)
        messages.success(self.request, "Transaction updated.")

        if getattr(self.request, "htmx", None):
            response = HttpResponse(status=204)
            trigger_client_event(response, "transactionUpdated", {})
            return response
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        if getattr(self.request, "htmx", None):
            return self.render_to_response(
                self.get_context_data(form=form), status=422
            )
        return super().form_invalid(form)


class TransactionDeleteView(FinanceViewMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy("finance:transaction-list")

    def post(self, request, *args, **kwargs):
        txn = self.get_object()
        service = TransactionService()
        service.delete_transaction(txn)
        messages.success(request, "Transaction deleted.")

        if getattr(request, "htmx", None):
            response = HttpResponse(status=200)
            trigger_client_event(response, "transactionDeleted", {"id": str(txn.id)})
            return response
        return HttpResponseRedirect(self.success_url)


class TransactionRowView(FinanceViewMixin, DetailView):
    """Return single transaction row (setelah inline edit)."""
    model = Transaction
    template_name = "finance/transactions/_row.html"


class TransactionFilterView(HtmxOnlyMixin, FinanceViewMixin, ListView):
    """HTMX-only: filtered transaction list partial."""
    model = Transaction
    template_name = "finance/transactions/_list_partial.html"
    context_object_name = "transactions"
    paginate_by = 25

    def get_queryset(self):
        repo = TransactionRepository()
        return repo.get_user_transactions(
            user=self.request.user,
            start_date=self.request.GET.get("start_date") or None,
            end_date=self.request.GET.get("end_date") or None,
            category_id=self.request.GET.get("category") or None,
            account_id=self.request.GET.get("account") or None,
            transaction_type=self.request.GET.get("type") or None,
            search=self.request.GET.get("q") or None,
        )


class TransactionImportView(FinanceViewMixin, View):
    template_name = "finance/transactions/import.html"

    def get(self, request):
        from django.shortcuts import render
        form = ImportForm(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        from django.shortcuts import render
        from apps.finance.models import FinancialAccount
        form = ImportForm(request.POST, request.FILES, user=request.user)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        csv_file = request.FILES["csv_file"]
        content = csv_file.read().decode("utf-8")
        account_id = form.cleaned_data["account"]

        try:
            account = FinancialAccount.objects.get(pk=account_id, user=request.user)
        except FinancialAccount.DoesNotExist:
            messages.error(request, "Account not found.")
            return render(request, self.template_name, {"form": form})

        importer = TransactionImportService()
        service = TransactionService()
        count = 0
        errors = []

        try:
            for row in importer.parse_csv(content):
                try:
                    service.create_transaction(
                        user=request.user,
                        account=account,
                        category=None,
                        transaction_type=row["transaction_type"],
                        amount=row["amount"],
                        date=row["date"],
                        description=row["description"],
                        payee=row.get("payee", ""),
                        notes=row.get("notes", ""),
                    )
                    count += 1
                except Exception as e:
                    errors.append(str(e))
        except ImportError as e:
            messages.error(request, str(e))
            return render(request, self.template_name, {"form": form})

        if errors:
            messages.warning(
                request,
                f"Imported {count} transactions with {len(errors)} errors."
            )
        else:
            messages.success(request, f"Successfully imported {count} transactions.")

        from django.shortcuts import redirect
        return redirect("finance:transaction-list")


class TransactionExportView(FinanceViewMixin, View):
    def get(self, request):
        import csv as csv_module
        from django.http import StreamingHttpResponse

        repo = TransactionRepository()
        transactions = repo.get_user_transactions(user=request.user)

        def generate():
            yield "date,description,amount,currency,type,payee,category,account\n"
            for txn in transactions.iterator(chunk_size=500):
                yield (
                    f"{txn.date},{txn.description},{txn.amount},{txn.currency},"
                    f"{txn.transaction_type},{txn.payee},"
                    f"{txn.category.name if txn.category else ''},"
                    f"{txn.account.name}\n"
                )

        response = StreamingHttpResponse(generate(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="transactions.csv"'
        return response
```

---

### 9.4 Budget Views

#### `apps/finance/views/budgets.py`

```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django_htmx.http import trigger_client_event

from apps.core.mixins import FinanceViewMixin
from apps.finance.models import Budget
from apps.finance.forms import BudgetForm
from apps.finance.services.budget_service import BudgetService


class BudgetListView(FinanceViewMixin, ListView):
    model = Budget
    template_name = "finance/budgets/list.html"
    context_object_name = "budgets"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["budgets_with_usage"] = BudgetService().get_active_budgets_with_usage(
            self.request.user
        )
        return ctx


class BudgetCreateView(FinanceViewMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = "finance/budgets/_form.html"
    success_url = reverse_lazy("finance:budget-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        budget = form.save()
        messages.success(self.request, "Budget created successfully.")

        if getattr(self.request, "htmx", None):
            response = HttpResponse(status=204)
            trigger_client_event(response, "budgetAdded", {})
            return response
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        if getattr(self.request, "htmx", None):
            return self.render_to_response(
                self.get_context_data(form=form), status=422
            )
        return super().form_invalid(form)


class BudgetUpdateView(FinanceViewMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "finance/budgets/_form.html"
    success_url = reverse_lazy("finance:budget-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Budget updated.")

        if getattr(self.request, "htmx", None):
            response = HttpResponse(status=204)
            trigger_client_event(response, "budgetUpdated", {})
            return response
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        if getattr(self.request, "htmx", None):
            return self.render_to_response(
                self.get_context_data(form=form), status=422
            )
        return super().form_invalid(form)


class BudgetDeleteView(FinanceViewMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy("finance:budget-list")

    def post(self, request, *args, **kwargs):
        budget = self.get_object()
        budget.delete()
        messages.success(request, "Budget deleted.")

        if getattr(request, "htmx", None):
            response = HttpResponse(status=200)
            trigger_client_event(response, "budgetDeleted", {"id": str(budget.id)})
            return response
        return HttpResponseRedirect(self.success_url)


class BudgetRowView(FinanceViewMixin, DetailView):
    """Return single budget row setelah inline edit."""
    model = Budget
    template_name = "finance/budgets/_budget_row.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        usage_list = BudgetService().get_active_budgets_with_usage(self.request.user)
        for item in usage_list:
            if item["budget"].pk == self.object.pk:
                ctx.update(item)
                break
        return ctx
```

---

### 9.5 Account Views

#### `apps/finance/views/accounts.py`

```python
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django_htmx.http import trigger_client_event

from apps.core.mixins import FinanceViewMixin
from apps.finance.models import FinancialAccount
from apps.finance.forms import AccountForm
from apps.finance.repositories.transaction_repo import TransactionRepository


class AccountListView(FinanceViewMixin, ListView):
    model = FinancialAccount
    template_name = "finance/accounts/list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        return FinancialAccount.objects.filter(
            user=self.request.user, is_active=True
        )


class AccountCreateView(FinanceViewMixin, CreateView):
    model = FinancialAccount
    form_class = AccountForm
    template_name = "finance/accounts/_form.html"
    success_url = reverse_lazy("finance:account-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Saldo awal = current balance
        account = form.save(commit=False)
        account.current_balance = account.initial_balance
        account.save()
        messages.success(self.request, "Account created.")

        if getattr(self.request, "htmx", None):
            response = HttpResponse(status=204)
            trigger_client_event(response, "accountAdded", {})
            return response
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        if getattr(self.request, "htmx", None):
            return self.render_to_response(
                self.get_context_data(form=form), status=422
            )
        return super().form_invalid(form)


class AccountUpdateView(FinanceViewMixin, UpdateView):
    model = FinancialAccount
    form_class = AccountForm
    template_name = "finance/accounts/_form.html"
    success_url = reverse_lazy("finance:account-list")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account updated.")

        if getattr(self.request, "htmx", None):
            response = HttpResponse(status=204)
            trigger_client_event(response, "accountUpdated", {})
            return response
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        if getattr(self.request, "htmx", None):
            return self.render_to_response(
                self.get_context_data(form=form), status=422
            )
        return super().form_invalid(form)


class AccountDetailView(FinanceViewMixin, DetailView):
    model = FinancialAccount
    template_name = "finance/accounts/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        repo = TransactionRepository()
        ctx["transactions"] = repo.get_user_transactions(
            user=self.request.user,
            account_id=str(self.object.pk),
        )[:20]
        return ctx
```

---

### 9.6 Report Views

#### `apps/finance/views/reports.py`

```python
from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils import timezone

from apps.core.mixins import HtmxMixin
from apps.finance.services.report_service import ReportService


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "finance/reports/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()
        # Default: bulan ini
        start = today.replace(day=1)
        end = today
        ctx["report"] = ReportService().get_summary(
            self.request.user, start, end
        )
        ctx["start_date"] = start
        ctx["end_date"] = end
        return ctx


class ReportDataView(LoginRequiredMixin, HtmxMixin, TemplateView):
    """HTMX: load report data untuk range tertentu."""
    template_name = "finance/reports/_report_data.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()

        start_str = self.request.GET.get("start_date")
        end_str = self.request.GET.get("end_date")

        try:
            from datetime import datetime
            start = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today.replace(day=1)
            end = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else today
        except ValueError:
            start = today.replace(day=1)
            end = today

        ctx["report"] = ReportService().get_summary(self.request.user, start, end)
        ctx["start_date"] = start
        ctx["end_date"] = end
        return ctx


class ReportExportCsvView(LoginRequiredMixin, View):
    def get(self, request):
        from django.http import StreamingHttpResponse
        from apps.finance.repositories.transaction_repo import TransactionRepository
        from datetime import datetime

        start_str = request.GET.get("start_date")
        end_str = request.GET.get("end_date")

        try:
            start = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else None
            end = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else None
        except ValueError:
            start = end = None

        repo = TransactionRepository()
        transactions = repo.get_user_transactions(
            user=request.user, start_date=start, end_date=end
        )

        def generate():
            yield "date,description,amount,currency,type,payee,category\n"
            for t in transactions.iterator(chunk_size=500):
                yield (
                    f"{t.date},{t.description},{t.amount},{t.currency},"
                    f"{t.transaction_type},{t.payee},"
                    f"{t.category.name if t.category else ''}\n"
                )

        response = StreamingHttpResponse(generate(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="report.csv"'
        return response
```

---

## FASE 10 — Templates Finance

### 10.1 Dashboard Template

#### `apps/finance/templates/finance/dashboard/index.html`

```html
{% extends "base.html" %}
{% load finance_tags %}

{% block title %}Dashboard — FinTrack{% endblock %}

{% block content %}
<div class="space-y-6">
  {# Header #}
  <div>
    <h1 class="text-2xl font-bold text-base-content">Dashboard</h1>
    <p class="text-base-content/60 text-sm">{{ today|date:"F Y" }} overview</p>
  </div>

  {# KPI Cards — auto-refreshed via polling #}
  <div
    id="kpi-cards"
    hx-get="{% url 'finance:dashboard-summary' %}"
    hx-trigger="every 60s"
    hx-swap="innerHTML"
  >
    {% include "finance/dashboard/_kpi_cards.html" %}
  </div>

  {# Bottom grid: Recent transactions + Budgets #}
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    {# Recent Transactions #}
    <div class="card bg-base-100 shadow-sm">
      <div class="card-body">
        <div class="flex items-center justify-between mb-4">
          <h2 class="card-title text-lg">Recent Transactions</h2>
          <a href="{% url 'finance:transaction-list' %}" class="btn btn-ghost btn-xs">
            View all →
          </a>
        </div>
        <div class="space-y-2">
          {% for txn in recent_transactions %}
            <div class="flex items-center justify-between py-2 border-b border-base-200 last:border-0">
              <div class="flex items-center gap-3">
                <div
                  class="w-8 h-8 rounded-full flex items-center justify-center text-sm"
                  style="background-color: {{ txn.category.color|default:'#6B7280' }}20; color: {{ txn.category.color|default:'#6B7280' }};"
                >
                  {{ txn.category.icon|default:"💰" }}
                </div>
                <div>
                  <p class="text-sm font-medium">{{ txn.description }}</p>
                  <p class="text-xs text-base-content/50">{{ txn.date|date:"d M" }}</p>
                </div>
              </div>
              <span class="font-mono text-sm {% if txn.is_income %}income{% else %}expense{% endif %}">
                {% if txn.is_income %}+{% else %}-{% endif %}{{ txn.amount|currency:txn.currency }}
              </span>
            </div>
          {% empty %}
            <p class="text-base-content/50 text-sm text-center py-4">No transactions yet</p>
          {% endfor %}
        </div>
      </div>
    </div>

    {# Budget Overview #}
    <div class="card bg-base-100 shadow-sm">
      <div class="card-body">
        <div class="flex items-center justify-between mb-4">
          <h2 class="card-title text-lg">Budget Status</h2>
          <a href="{% url 'finance:budget-list' %}" class="btn btn-ghost btn-xs">
            Manage →
          </a>
        </div>
        <div class="space-y-4">
          {% for item in budgets %}
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="font-medium">{{ item.budget.name }}</span>
                <span class="{% if item.is_over %}text-error{% elif item.percentage >= 80 %}text-warning{% else %}text-base-content/60{% endif %}">
                  {{ item.spent|currency:item.budget.currency }} /
                  {{ item.budget.amount|currency:item.budget.currency }}
                </span>
              </div>
              <progress
                class="progress w-full {% budget_progress_color item.percentage %}"
                value="{{ item.percentage|floatformat:0 }}"
                max="100"
              ></progress>
              <p class="text-xs text-base-content/50 text-right">
                {{ item.percentage|percentage }} used
              </p>
            </div>
          {% empty %}
            <p class="text-base-content/50 text-sm text-center py-4">No budgets set</p>
          {% endfor %}
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

#### `apps/finance/templates/finance/dashboard/_kpi_cards.html`

```html
{% load finance_tags %}
<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
  {# Income #}
  <div class="stat bg-base-100 rounded-2xl shadow-sm">
    <div class="stat-figure text-success">
      <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M7 11l5-5m0 0l5 5m-5-5v12"/>
      </svg>
    </div>
    <div class="stat-title text-base-content/60">Income</div>
    <div class="stat-value text-success text-2xl">
      {{ summary.total_income|currency:base_currency }}
    </div>
    <div class="stat-desc">This month</div>
  </div>

  {# Expense #}
  <div class="stat bg-base-100 rounded-2xl shadow-sm">
    <div class="stat-figure text-error">
      <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17 13l-5 5m0 0l-5-5m5 5V6"/>
      </svg>
    </div>
    <div class="stat-title text-base-content/60">Expenses</div>
    <div class="stat-value text-error text-2xl">
      {{ summary.total_expense|currency:base_currency }}
    </div>
    <div class="stat-desc">This month</div>
  </div>

  {# Net #}
  <div class="stat bg-base-100 rounded-2xl shadow-sm">
    <div class="stat-figure {% if summary.net >= 0 %}text-success{% else %}text-error{% endif %}">
      <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
    </div>
    <div class="stat-title text-base-content/60">Net</div>
    <div class="stat-value {% if summary.net >= 0 %}text-success{% else %}text-error{% endif %} text-2xl">
      {{ summary.net|currency:base_currency }}
    </div>
    <div class="stat-desc">Income - Expenses</div>
  </div>
</div>
```

---

### 10.2 Transaction List & Partials

#### `apps/finance/templates/finance/transactions/list.html`

```html
{% extends "base.html" %}
{% load finance_tags %}

{% block title %}Transactions — FinTrack{% endblock %}

{% block content %}
<div class="space-y-6">
  {# Header #}
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-2xl font-bold">Transactions</h1>
      <p class="text-base-content/60 text-sm">Manage your income and expenses</p>
    </div>
    <div class="flex gap-2">
      <a href="{% url 'finance:transaction-import' %}" class="btn btn-outline btn-sm gap-1">
        📂 Import CSV
      </a>
      <a href="{% url 'finance:transaction-export' %}" class="btn btn-outline btn-sm gap-1">
        📥 Export
      </a>
      <button
        class="btn btn-primary gap-2"
        hx-get="{% url 'finance:transaction-create' %}"
        hx-target="#modal-container"
        hx-swap="innerHTML"
        _="on htmx:afterSwap call document.getElementById('txn-modal').showModal()"
      >
        + Add Transaction
      </button>
    </div>
  </div>

  {# Filters #}
  <div class="card bg-base-100 shadow-sm">
    <div class="card-body py-4">
      <form
        id="filter-form"
        hx-get="{% url 'finance:transaction-filter' %}"
        hx-target="#transaction-list"
        hx-swap="innerHTML"
        hx-trigger="change from:select, input from:[type=date] delay:300ms, keyup from:[type=search] delay:400ms"
        hx-push-url="true"
        hx-indicator="#filter-spinner"
      >
        {% include "finance/transactions/_filters.html" %}
      </form>
    </div>
  </div>

  {# Transaction List #}
  <div id="transaction-list">
    {% include "finance/transactions/_list_partial.html" %}
  </div>
</div>

{# Modal #}
<dialog id="txn-modal" class="modal">
  <div class="modal-box w-11/12 max-w-2xl">
    <div id="modal-container"></div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
{% endblock %}

{% block extra_scripts %}
<script>
  htmx.on("transactionAdded", () => {
    document.getElementById("txn-modal").close();
    htmx.trigger("#transaction-list", "refresh");
  });
  htmx.on("transactionUpdated", () => {
    document.getElementById("txn-modal").close();
    htmx.trigger("#transaction-list", "refresh");
  });
  htmx.on("transactionDeleted", (evt) => {
    const row = document.getElementById(`txn-row-${evt.detail.id}`);
    if (row) {
      row.classList.add("opacity-0", "transition-opacity", "duration-300");
      setTimeout(() => row.remove(), 300);
    }
  });
</script>
{% endblock %}
```

#### `apps/finance/templates/finance/transactions/_filters.html`

```html
{% load widget_tweaks %}
<div class="flex flex-wrap gap-3 items-end">
  {# Search #}
  <div class="form-control flex-1 min-w-48">
    <label class="label py-1"><span class="label-text text-xs">Search</span></label>
    <input
      type="search"
      name="q"
      value="{{ filters.q }}"
      placeholder="Search transactions..."
      class="input input-bordered input-sm"
      hx-get="{% url 'finance:transaction-filter' %}"
      hx-trigger="keyup changed delay:400ms, search"
      hx-target="#transaction-list"
      hx-swap="innerHTML"
      hx-indicator="#filter-spinner"
    />
  </div>

  {# Date range #}
  <div class="form-control">
    <label class="label py-1"><span class="label-text text-xs">From</span></label>
    <input type="date" name="start_date" value="{{ filters.start_date }}"
           class="input input-bordered input-sm" />
  </div>
  <div class="form-control">
    <label class="label py-1"><span class="label-text text-xs">To</span></label>
    <input type="date" name="end_date" value="{{ filters.end_date }}"
           class="input input-bordered input-sm" />
  </div>

  {# Type #}
  <div class="form-control">
    <label class="label py-1"><span class="label-text text-xs">Type</span></label>
    <select name="type" class="select select-bordered select-sm">
      <option value="">All types</option>
      <option value="income" {% if filters.type == "income" %}selected{% endif %}>Income</option>
      <option value="expense" {% if filters.type == "expense" %}selected{% endif %}>Expense</option>
      <option value="transfer" {% if filters.type == "transfer" %}selected{% endif %}>Transfer</option>
    </select>
  </div>

  {# Spinner #}
  <span id="filter-spinner" class="htmx-indicator loading loading-spinner loading-sm"></span>
</div>
```

#### `apps/finance/templates/finance/transactions/_list_partial.html`

```html
{% load finance_tags %}
<div class="card bg-base-100 shadow-sm overflow-hidden">
  <div class="overflow-x-auto">
    <table class="table table-zebra w-full">
      <thead>
        <tr class="text-base-content/60 text-xs uppercase tracking-wide">
          <th class="w-8"><input type="checkbox" class="checkbox checkbox-sm" id="select-all" /></th>
          <th>Date</th>
          <th>Category</th>
          <th>Description</th>
          <th>Account</th>
          <th class="text-right">Amount</th>
          <th class="text-right">Actions</th>
        </tr>
      </thead>
      <tbody id="transactions-tbody">
        {% for transaction in transactions %}
          {% include "finance/transactions/_row.html" %}
        {% empty %}
          <tr>
            <td colspan="7" class="text-center py-12 text-base-content/40">
              <div class="flex flex-col items-center gap-2">
                <span class="text-4xl">💸</span>
                <p>No transactions found</p>
                <p class="text-sm">Add your first transaction to get started</p>
              </div>
            </td>
          </tr>
        {% endfor %}

        {# Infinite scroll trigger #}
        {% if page_obj.has_next %}
          <tr
            hx-get="?page={{ page_obj.next_page_number }}&{{ request.GET.urlencode }}"
            hx-trigger="intersect once"
            hx-target="this"
            hx-swap="afterend"
            hx-indicator="#scroll-spinner"
          >
            <td colspan="7" class="text-center py-4" id="scroll-trigger">
              <span id="scroll-spinner" class="htmx-indicator loading loading-spinner loading-sm"></span>
            </td>
          </tr>
        {% endif %}
      </tbody>
    </table>
  </div>
</div>
```

#### `apps/finance/templates/finance/transactions/_row.html`

```html
{% load finance_tags %}
<tr
  id="txn-row-{{ transaction.id }}"
  class="hover:bg-base-200 transition-colors group"
>
  <td class="w-8">
    <input type="checkbox" class="checkbox checkbox-sm" name="txn-ids" value="{{ transaction.id }}" />
  </td>
  <td>
    <span class="text-sm text-base-content/70">{{ transaction.date|date:"d M Y" }}</span>
  </td>
  <td>
    {% if transaction.category %}
      <div
        class="badge badge-sm font-normal"
        style="background-color: {{ transaction.category.color }}20; color: {{ transaction.category.color }}; border-color: {{ transaction.category.color }}40;"
      >
        {{ transaction.category.icon }} {{ transaction.category.name }}
      </div>
    {% else %}
      <span class="text-base-content/30 text-sm">—</span>
    {% endif %}
  </td>
  <td class="max-w-xs">
    <p class="truncate text-sm font-medium">{{ transaction.description }}</p>
    {% if transaction.payee %}
      <p class="text-xs text-base-content/50 truncate">{{ transaction.payee }}</p>
    {% endif %}
  </td>
  <td>
    <span class="badge badge-outline badge-sm">{{ transaction.account.name }}</span>
  </td>
  <td class="text-right font-mono font-semibold {% if transaction.is_income %}text-success{% else %}text-error{% endif %}">
    {% if transaction.is_income %}+{% else %}-{% endif %}{{ transaction.amount|currency:transaction.currency }}
  </td>
  <td>
    <div class="flex gap-1 justify-end opacity-0 group-hover:opacity-100 transition-opacity">
      <button
        class="btn btn-ghost btn-xs"
        hx-get="{% url 'finance:transaction-update' transaction.pk %}"
        hx-target="#modal-container"
        hx-swap="innerHTML"
        _="on htmx:afterSwap call document.getElementById('txn-modal').showModal()"
        title="Edit"
      >✏️</button>
      <button
        class="btn btn-ghost btn-xs text-error"
        hx-delete="{% url 'finance:transaction-delete' transaction.pk %}"
        hx-confirm="Delete '{{ transaction.description }}'? This cannot be undone."
        title="Delete"
      >🗑️</button>
    </div>
  </td>
</tr>
```

#### `apps/finance/templates/finance/transactions/_form.html`

```html
{% load widget_tweaks %}
<div class="p-1">
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-lg font-bold">
      {% if form.instance.pk %}Edit Transaction{% else %}New Transaction{% endif %}
    </h3>
    <button
      type="button"
      class="btn btn-ghost btn-sm btn-circle"
      _="on click call document.getElementById('txn-modal').close()"
    >✕</button>
  </div>

  <form
    {% if form.instance.pk %}
      hx-post="{% url 'finance:transaction-update' form.instance.pk %}"
    {% else %}
      hx-post="{% url 'finance:transaction-create' %}"
    {% endif %}
    hx-indicator="#form-spinner"
  >
    {% csrf_token %}

    {# Errors #}
    {% if form.non_field_errors %}
      <div class="alert alert-error mb-4">
        {% for error in form.non_field_errors %}
          <p class="text-sm">{{ error }}</p>
        {% endfor %}
      </div>
    {% endif %}

    <div class="grid grid-cols-2 gap-4">
      <div class="form-control col-span-2">
        <label class="label"><span class="label-text font-medium">Type</span></label>
        {{ form.transaction_type }}
        {% if form.transaction_type.errors %}
          <label class="label"><span class="label-text-alt text-error">{{ form.transaction_type.errors|first }}</span></label>
        {% endif %}
      </div>

      <div class="form-control col-span-2 sm:col-span-1">
        <label class="label"><span class="label-text font-medium">Account</span></label>
        {{ form.account }}
        {% if form.account.errors %}
          <label class="label"><span class="label-text-alt text-error">{{ form.account.errors|first }}</span></label>
        {% endif %}
      </div>

      <div class="form-control col-span-2 sm:col-span-1">
        <label class="label"><span class="label-text font-medium">Category</span></label>
        {{ form.category }}
      </div>

      <div class="form-control col-span-2 sm:col-span-1">
        <label class="label"><span class="label-text font-medium">Amount</span></label>
        {{ form.amount }}
        {% if form.amount.errors %}
          <label class="label"><span class="label-text-alt text-error">{{ form.amount.errors|first }}</span></label>
        {% endif %}
      </div>

      <div class="form-control col-span-2 sm:col-span-1">
        <label class="label"><span class="label-text font-medium">Date</span></label>
        {{ form.date }}
        {% if form.date.errors %}
          <label class="label"><span class="label-text-alt text-error">{{ form.date.errors|first }}</span></label>
        {% endif %}
      </div>

      <div class="form-control col-span-2">
        <label class="label"><span class="label-text font-medium">Description</span></label>
        {{ form.description }}
        {% if form.description.errors %}
          <label class="label"><span class="label-text-alt text-error">{{ form.description.errors|first }}</span></label>
        {% endif %}
      </div>

      <div class="form-control col-span-2 sm:col-span-1">
        <label class="label"><span class="label-text font-medium">Payee (optional)</span></label>
        {{ form.payee }}
      </div>

      <div class="form-control col-span-2 sm:col-span-1">
        <label class="label"><span class="label-text font-medium">Status</span></label>
        {{ form.status }}
      </div>

      <div class="form-control col-span-2">
        <label class="label"><span class="label-text font-medium">Notes (optional)</span></label>
        {{ form.notes }}
        <label class="label">
          <span class="label-text-alt"
                _="on keyup put (500 - closest <textarea/>.value.length) + ' chars left' into me.textContent">
            500 chars left
          </span>
        </label>
      </div>
    </div>

    <div class="flex gap-3 justify-end mt-6">
      <button
        type="button"
        class="btn btn-ghost"
        _="on click call document.getElementById('txn-modal').close()"
      >Cancel</button>
      <button type="submit" class="btn btn-primary gap-2">
        <span id="form-spinner" class="htmx-indicator loading loading-spinner loading-xs"></span>
        {% if form.instance.pk %}Update{% else %}Save{% endif %}
      </button>
    </div>
  </form>
</div>
```

---

### 10.3 Budget Templates

#### `apps/finance/templates/finance/budgets/list.html`

```html
{% extends "base.html" %}
{% load finance_tags %}

{% block title %}Budgets — FinTrack{% endblock %}

{% block content %}
<div class="space-y-6">
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-2xl font-bold">Budgets</h1>
      <p class="text-base-content/60 text-sm">Track your spending limits</p>
    </div>
    <button
      class="btn btn-primary gap-2"
      hx-get="{% url 'finance:budget-create' %}"
      hx-target="#budget-modal-container"
      hx-swap="innerHTML"
      _="on htmx:afterSwap call document.getElementById('budget-modal').showModal()"
    >
      + Add Budget
    </button>
  </div>

  {# Budget cards #}
  <div id="budget-list" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
    {% for item in budgets_with_usage %}
      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <h3 class="font-bold">{{ item.budget.name }}</h3>
            <div class="dropdown dropdown-end">
              <button tabindex="0" class="btn btn-ghost btn-xs">⋮</button>
              <ul tabindex="0" class="dropdown-content z-[1] menu p-1 shadow bg-base-100 rounded-box w-36">
                <li>
                  <a
                    hx-get="{% url 'finance:budget-update' item.budget.pk %}"
                    hx-target="#budget-modal-container"
                    hx-swap="innerHTML"
                    _="on htmx:afterSwap call document.getElementById('budget-modal').showModal()"
                  >Edit</a>
                </li>
                <li>
                  <a
                    class="text-error"
                    hx-delete="{% url 'finance:budget-delete' item.budget.pk %}"
                    hx-confirm="Delete '{{ item.budget.name }}'?"
                  >Delete</a>
                </li>
              </ul>
            </div>
          </div>

          <div class="badge badge-outline badge-sm">{{ item.budget.category.name }}</div>

          <div class="mt-3">
            <div class="flex justify-between text-sm mb-1">
              <span>{{ item.spent|currency:item.budget.currency }}</span>
              <span class="text-base-content/60">{{ item.budget.amount|currency:item.budget.currency }}</span>
            </div>
            <progress
              class="progress w-full {% budget_progress_color item.percentage %}"
              value="{{ item.percentage|floatformat:0 }}"
              max="100"
            ></progress>
          </div>

          <div class="flex justify-between text-xs text-base-content/50 mt-1">
            <span>{{ item.percentage|percentage }} used</span>
            <span>{{ item.remaining|currency:item.budget.currency }} left</span>
          </div>

          {% if item.is_over %}
            <div class="alert alert-error py-2 mt-2">
              <span class="text-xs">⚠️ Over budget by {{ item.spent|subtract:item.budget.amount|currency:item.budget.currency }}</span>
            </div>
          {% endif %}
        </div>
      </div>
    {% empty %}
      <div class="col-span-full text-center py-12 text-base-content/40">
        <span class="text-4xl block mb-2">📊</span>
        <p>No budgets yet</p>
        <p class="text-sm">Create a budget to start tracking your spending</p>
      </div>
    {% endfor %}
  </div>
</div>

{# Budget Modal #}
<dialog id="budget-modal" class="modal">
  <div class="modal-box w-11/12 max-w-lg">
    <div id="budget-modal-container"></div>
  </div>
  <form method="dialog" class="modal-backdrop"><button>close</button></form>
</dialog>
{% endblock %}

{% block extra_scripts %}
<script>
  htmx.on("budgetAdded", () => {
    document.getElementById("budget-modal").close();
    htmx.trigger("#budget-list", "refresh");
  });
  htmx.on("budgetUpdated", () => {
    document.getElementById("budget-modal").close();
    location.reload();
  });
  htmx.on("budgetDeleted", () => location.reload());
</script>
{% endblock %}
```

---

## FASE 11 — HTMX Patterns

### 11.1 Infinite Scroll

Sudah diimplementasi di `_list_partial.html` — trigger `intersect once` pada baris terakhir.

### 11.2 Inline Edit

Contoh inline edit untuk budget amount:

```html
{# Display mode #}
<span
  id="budget-amount-{{ budget.pk }}"
  class="cursor-pointer hover:text-primary underline underline-offset-2"
  hx-get="{% url 'finance:budget-update' budget.pk %}?field=amount"
  hx-target="this"
  hx-swap="outerHTML"
>
  {{ budget.amount|currency:budget.currency }}
</span>
```

### 11.3 OOB Swaps

Sudah diimplementasi di views `form_valid` — menggunakan `trigger_client_event` dari django-htmx.

Contoh OOB update account balance:

```python
# Di views.py setelah transaction berhasil dibuat:
from django.template.loader import render_to_string
from django.http import HttpResponse

def form_valid(self, form):
    txn = service.create_transaction(...)

    if getattr(self.request, "htmx", None):
        account_html = render_to_string(
            "finance/accounts/_balance_widget.html",
            {"account": txn.account},
            request=self.request,
        )
        response = HttpResponse(
            f'<div id="account-balance-{txn.account.pk}" hx-swap-oob="true">'
            f'{account_html}</div>',
            status=204,
        )
        trigger_client_event(response, "transactionAdded", {})
        return response
```

### 11.4 Live Search & Filter

Sudah diimplementasi di `_filters.html` — `hx-trigger="keyup changed delay:400ms"`.

### 11.5 Polling Dashboard

Sudah diimplementasi di `dashboard/index.html` — `hx-trigger="every 60s"`.

---

## FASE 12 — Celery & Background Tasks

### 12.1 Instalasi & Konfigurasi Celery

Celery sudah dikonfigurasi di `config/celery.py` dan `config/__init__.py`. Untuk menjalankan:

```bash
# Terminal 1: Django dev server
uv run python manage.py runserver

# Terminal 2: Celery worker
uv run celery -A config worker -l info

# Terminal 3: Celery beat (scheduler)
uv run celery -A config beat -l info

# Opsional: Flower (monitoring Celery)
uv add flower
uv run celery -A config flower --port=5555
```

---

### 12.2 Recurring Transaction Task

#### `apps/finance/tasks.py`

```python
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
    name="finance.generate_recurring_transactions",
)
def generate_recurring_transactions(self):
    """Jalankan setiap hari via Celery Beat — buat transaksi dari template recurring."""
    from apps.finance.models import RecurringTransaction
    from apps.finance.services.transaction_service import TransactionService

    today = timezone.localdate()
    service = TransactionService()
    count = 0

    due = RecurringTransaction.objects.filter(
        is_active=True,
        next_due_date__lte=today,
    ).select_related("user", "account", "category")

    for recurring in due:
        try:
            service.create_from_recurring(recurring, date=today)
            recurring.advance_next_due_date()
            count += 1
        except Exception as exc:
            logger.error(f"Failed to generate recurring {recurring.pk}: {exc}")

    logger.info(f"Generated {count} recurring transactions for {today}")
    return count


@shared_task(name="finance.refresh_exchange_rates")
def refresh_exchange_rates():
    """Refresh FX rates dari API eksternal."""
    from apps.finance.services.currency_service import CurrencyService
    CurrencyService().refresh_all_rates()


@shared_task(name="finance.send_budget_alert")
def send_budget_alert(budget_id: str, user_id: int, percentage: float):
    """Kirim notifikasi budget overage."""
    from apps.finance.models import Budget
    from apps.notifications.services import NotificationService

    try:
        budget = Budget.objects.select_related("user", "category").get(pk=budget_id)
        NotificationService().send_budget_alert(budget, percentage)
    except Budget.DoesNotExist:
        logger.error(f"Budget {budget_id} not found for alert")
```

---

### 12.3 Exchange Rate Task

Sudah diimplementasi di `tasks.py` dan `CurrencyService.refresh_all_rates()`.

---

### 12.4 Budget Alert Task

Sudah diimplementasi di `tasks.py` dan `BudgetService._send_budget_alert()`.

---

## FASE 13 — Caching & Performance

### 13.1 Redis Cache Setup

Sudah dikonfigurasi di `production.py`. Untuk development, tambahkan ke `development.py`:

```python
# development.py — tambahkan jika Redis tersedia
# Kalau tidak ada Redis, gunakan LocMemCache (default)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
```

---

### 13.2 View-level & Query-level Cache

```python
# apps/finance/views/dashboard.py — tambahkan cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 5, key_prefix="dashboard-summary"), name="dispatch")
class DashboardSummaryView(LoginRequiredMixin, HtmxMixin, TemplateView):
    # ... implementasi sama seperti sebelumnya
```

**Template fragment cache:**

```html
{% load cache %}
{% cache 3600 "category-dropdown" request.user.pk %}
  <select name="category" class="select select-bordered w-full">
    <option value="">— All categories —</option>
    {% for cat in categories %}
      <option value="{{ cat.pk }}">{{ cat.name }}</option>
    {% endfor %}
  </select>
{% endcache %}
```

---

### 13.3 QuerySet Optimization

Semua repository sudah menggunakan `select_related` dan `prefetch_related`. Pastikan selalu:

```python
# ✅ BENAR
Transaction.objects.select_related("account", "category", "user")
Transaction.objects.prefetch_related("tags")

# ✅ Untuk list view — batasi kolom
Transaction.objects.only("id", "date", "description", "amount", "currency", "transaction_type")

# ✅ Untuk export besar — gunakan iterator
for txn in Transaction.objects.filter(user=user).iterator(chunk_size=1000):
    writer.writerow(...)

# ❌ HINDARI N+1
for txn in Transaction.objects.all():
    print(txn.account.name)  # ← N+1 query!
```

---

## FASE 14 — Notifications

### 14.1 Notification Model & Service

#### `apps/notifications/services.py`

```python
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationService:
    def create(
        self,
        user: User,
        notification_type: str,
        title: str,
        message: str,
        url: str = "",
    ) -> Notification:
        return Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            url=url,
        )

    def send_budget_alert(self, budget, percentage: float) -> None:
        self.create(
            user=budget.user,
            notification_type=Notification.TYPE_BUDGET_ALERT,
            title=f"Budget Alert: {budget.name}",
            message=(
                f"You've used {percentage:.1f}% of your '{budget.name}' budget "
                f"({budget.category.name}). "
                f"Remaining: {budget.amount - (budget.amount * percentage / 100):.0f} {budget.currency}."
            ),
            url="/budgets/",
        )

    def send_large_transaction_alert(self, transaction, threshold: float) -> None:
        self.create(
            user=transaction.user,
            notification_type=Notification.TYPE_LARGE_TRANSACTION,
            title=f"Large Transaction: {transaction.description}",
            message=(
                f"A large {transaction.transaction_type} of "
                f"{transaction.amount} {transaction.currency} was recorded."
            ),
            url=f"/transactions/{transaction.pk}/",
        )
```

---

### 14.2 In-app Notification Views

#### `apps/notifications/views.py`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/list.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class MarkReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        Notification.objects.filter(pk=pk, user=request.user).update(is_read=True)
        if getattr(request, "htmx", None):
            return HttpResponse(status=204)
        return HttpResponseRedirect(reverse_lazy("notifications:list"))


class MarkAllReadView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        if getattr(request, "htmx", None):
            return HttpResponse(status=204)
        return HttpResponseRedirect(reverse_lazy("notifications:list"))
```

---

### 14.3 Email Notification

Kirim email menggunakan Django's built-in email system. Tambahkan ke `NotificationService`:

```python
from django.core.mail import send_mail
from django.conf import settings

def send_budget_alert_email(self, budget, percentage: float) -> None:
    """Kirim email untuk budget alert."""
    send_mail(
        subject=f"[FinTrack] Budget Alert: {budget.name}",
        message=(
            f"Hi {budget.user.get_full_name() or budget.user.email},\n\n"
            f"You've used {percentage:.1f}% of your '{budget.name}' budget.\n"
            f"Category: {budget.category.name}\n"
            f"Budget: {budget.amount} {budget.currency}\n\n"
            f"Visit FinTrack to manage your budgets."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[budget.user.email],
        fail_silently=True,
    )
```

---

## FASE 15 — Testing

### 15.1 Setup pytest-django

Sudah dikonfigurasi di `pyproject.toml` section `[tool.pytest.ini_options]`.

```bash
# Jalankan semua tests
uv run pytest

# Dengan coverage
uv run pytest --cov

# Hanya unit tests
uv run pytest tests/unit/

# Dengan verbose output
uv run pytest -v

# Parallel (4 workers)
uv run pytest -n 4
```

---

### 15.2 Factories (factory-boy)

#### `tests/factories/__init__.py`

```python
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from apps.finance.models import (
    Transaction, FinancialAccount, Category, Budget, Tag
)

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_onboarded = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs.setdefault("password", "testpass123")
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class FinancialAccountFactory(DjangoModelFactory):
    class Meta:
        model = FinancialAccount

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Account {n}")
    account_type = FinancialAccount.TYPE_BANK
    currency = "IDR"
    initial_balance = factory.Faker(
        "pydecimal", left_digits=8, right_digits=2, positive=True
    )
    current_balance = factory.LazyAttribute(lambda o: o.initial_balance)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Category {n}")
    category_type = Category.TYPE_EXPENSE
    is_system = False


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    account = factory.SubFactory(
        FinancialAccountFactory,
        user=factory.SelfAttribute("..user")
    )
    category = factory.SubFactory(
        CategoryFactory,
        user=factory.SelfAttribute("..user"),
        category_type="expense",
    )
    transaction_type = Transaction.TYPE_EXPENSE
    amount = factory.Faker(
        "pydecimal", left_digits=6, right_digits=2, positive=True
    )
    currency = "IDR"
    date = factory.Faker("date_this_year")
    description = factory.Faker("sentence", nb_words=4)
    status = Transaction.STATUS_CLEARED


class BudgetFactory(DjangoModelFactory):
    class Meta:
        model = Budget

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Budget {n}")
    category = factory.SubFactory(
        CategoryFactory,
        user=factory.SelfAttribute("..user"),
        category_type="expense",
    )
    amount = factory.Faker(
        "pydecimal", left_digits=7, right_digits=2, positive=True
    )
    currency = "IDR"
    period = Budget.PERIOD_MONTHLY
    start_date = factory.Faker("date_this_year")
    is_active = True
```

---

### 15.3 Unit Tests

#### `tests/conftest.py`

```python
import pytest
from django.test import Client
from tests.factories import UserFactory, TransactionFactory, FinancialAccountFactory


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def auth_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def account(user, db):
    return FinancialAccountFactory(user=user)


@pytest.fixture
def transaction(user, account, db):
    return TransactionFactory(user=user, account=account)
```

#### `tests/unit/test_transaction_service.py`

```python
import pytest
from decimal import Decimal
from apps.finance.services.transaction_service import TransactionService
from apps.finance.models import Transaction


@pytest.mark.django_db
class TestTransactionService:

    def test_create_expense_decreases_account_balance(self, user, account):
        initial = account.current_balance
        service = TransactionService()

        service.create_transaction(
            user=user,
            account=account,
            category=None,
            transaction_type=Transaction.TYPE_EXPENSE,
            amount=Decimal("50000"),
            date="2026-01-15",
            description="Test expense",
        )

        account.refresh_from_db()
        assert account.current_balance == initial - Decimal("50000")

    def test_create_income_increases_account_balance(self, user, account):
        initial = account.current_balance
        service = TransactionService()

        service.create_transaction(
            user=user,
            account=account,
            category=None,
            transaction_type=Transaction.TYPE_INCOME,
            amount=Decimal("1000000"),
            date="2026-01-15",
            description="Salary",
        )

        account.refresh_from_db()
        assert account.current_balance == initial + Decimal("1000000")

    def test_delete_transaction_reverses_balance(self, user, account, transaction):
        balance_before = account.current_balance
        service = TransactionService()
        service.delete_transaction(transaction)
        account.refresh_from_db()
        # Expense dihapus → balance kembali naik
        assert account.current_balance == balance_before + transaction.amount

    def test_soft_delete_marks_deleted_at(self, user, account, transaction):
        service = TransactionService()
        service.delete_transaction(transaction)
        transaction.refresh_from_db()
        # SoftDelete: masih ada di DB tapi deleted_at terisi
        from apps.finance.models import Transaction as T
        assert T.all_objects.filter(pk=transaction.pk).exists()
        # Tidak muncul di query normal
        assert not T.objects.filter(pk=transaction.pk).exists()
```

---

### 15.4 Integration Tests (HTMX)

#### `tests/integration/test_transaction_views.py`

```python
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestTransactionCreateView:

    def test_htmx_create_returns_204_on_success(self, auth_client, account):
        url = reverse("finance:transaction-create")
        from django.utils import timezone

        response = auth_client.post(
            url,
            data={
                "transaction_type": "expense",
                "account": str(account.pk),
                "amount": "50000",
                "date": str(timezone.localdate()),
                "description": "Test lunch",
                "status": "cleared",
            },
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 204
        assert "HX-Trigger" in response.headers

    def test_htmx_create_invalid_returns_422(self, auth_client, account):
        url = reverse("finance:transaction-create")
        response = auth_client.post(
            url,
            data={"amount": "-100"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 422

    def test_non_htmx_create_redirects(self, auth_client, account):
        url = reverse("finance:transaction-create")
        from django.utils import timezone

        response = auth_client.post(
            url,
            data={
                "transaction_type": "expense",
                "account": str(account.pk),
                "amount": "50000",
                "date": str(timezone.localdate()),
                "description": "Test expense",
                "status": "cleared",
            },
        )
        assert response.status_code == 302


@pytest.mark.django_db
class TestTransactionListView:

    def test_list_requires_login(self, client):
        url = reverse("finance:transaction-list")
        response = client.get(url)
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_list_returns_200_for_authenticated(self, auth_client):
        url = reverse("finance:transaction-list")
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_user_only_sees_own_transactions(self, auth_client, user, account, db):
        from tests.factories import UserFactory, TransactionFactory, FinancialAccountFactory
        other_user = UserFactory()
        other_account = FinancialAccountFactory(user=other_user)
        other_txn = TransactionFactory(user=other_user, account=other_account)

        url = reverse("finance:transaction-list")
        response = auth_client.get(url)
        content = response.content.decode()
        assert other_txn.description not in content
```

---

## FASE 16 — Security

### 16.1 Django Security Settings

Sudah dikonfigurasi di `production.py` (lihat Fase 1.4).

---

### 16.2 HTMX Security Middleware

Tambahkan `HtmxSecurityMiddleware` ke MIDDLEWARE di production settings:

```python
# production.py
MIDDLEWARE += [
    "apps.core.middleware.HtmxSecurityMiddleware",
]
```

---

### 16.3 Rate Limiting

```python
# apps/finance/views/transactions.py — tambahkan decorator
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


@method_decorator(
    ratelimit(key="user", rate="60/m", method="POST", block=True),
    name="dispatch"
)
class TransactionCreateView(FinanceViewMixin, CreateView):
    # ... implementasi sama
```

---

### 16.4 CSP Headers

Sudah dikonfigurasi di `production.py`. Untuk development, tambahkan middleware:

```python
# base.py — setelah WhiteNoise
MIDDLEWARE += [
    "csp.middleware.CSPMiddleware",
]
```

---

## FASE 17 — Deployment

### 17.1 Dockerfile & Docker Compose

#### `docker/Dockerfile`

```dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install Node.js untuk django-tailwind
RUN apt-get update && apt-get install -y nodejs npm curl && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install Python dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy source
COPY . .

# Build Tailwind CSS
RUN uv run python manage.py tailwind install --no-input
RUN uv run python manage.py tailwind build --no-input

# Collect static files
RUN DJANGO_SETTINGS_MODULE=config.settings.production \
    DJANGO_SECRET_KEY=build-time-secret \
    uv run python manage.py collectstatic --noinput

# ── Web (Gunicorn) ────────────────────────────────────────────
FROM base AS web
EXPOSE 8000
CMD ["uv", "run", "gunicorn", "config.wsgi:application",
     "--bind", "0.0.0.0:8000",
     "--workers", "4",
     "--worker-class", "gthread",
     "--threads", "2",
     "--timeout", "120",
     "--access-logfile", "-",
     "--error-logfile", "-"]

# ── Celery Worker ─────────────────────────────────────────────
FROM base AS worker
CMD ["uv", "run", "celery", "-A", "config", "worker",
     "-l", "info", "-c", "4", "--max-tasks-per-child", "1000"]

# ── Celery Beat ───────────────────────────────────────────────
FROM base AS beat
CMD ["uv", "run", "celery", "-A", "config", "beat",
     "-l", "info", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"]
```

#### `docker/docker-compose.yml` (development)

```yaml
version: "3.9"

services:
  web:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      target: base
    command: uv run python manage.py runserver 0.0.0.0:8000
    volumes:
      - ..:/app
    ports:
      - "8000:8000"
    env_file: ../.env
    depends_on:
      - postgres
      - redis
    environment:
      DJANGO_SETTINGS_MODULE: config.settings.development

  tailwind:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      target: base
    command: uv run python manage.py tailwind start
    volumes:
      - ..:/app
    depends_on:
      - web

  worker:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      target: base
    command: uv run celery -A config worker -l info
    volumes:
      - ..:/app
    env_file: ../.env
    depends_on:
      - postgres
      - redis

  beat:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      target: base
    command: uv run celery -A config beat -l info
    volumes:
      - ..:/app
    env_file: ../.env
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: fintrack_db
      POSTGRES_USER: fintrack
      POSTGRES_PASSWORD: devpassword
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

#### `docker/docker-compose.prod.yml`

```yaml
version: "3.9"

services:
  web:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      target: web
    env_file: ../.env
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    networks: [fintrack]

  worker:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      target: worker
    env_file: ../.env
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    networks: [fintrack]

  beat:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      target: beat
    env_file: ../.env
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    networks: [fintrack]

  postgres:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: fintrack_db
      POSTGRES_USER: fintrack
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    restart: unless-stopped
    networks: [fintrack]

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks: [fintrack]

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ../staticfiles:/static:ro
      - ../media:/media:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on: [web]
    restart: unless-stopped
    networks: [fintrack]

volumes:
  postgres_data:
  redis_data:

networks:
  fintrack:
    driver: bridge
```

---

### 17.2 Nginx Configuration

#### `docker/nginx/nginx.conf`

```nginx
upstream fintrack {
    server web:8000;
}

server {
    listen 80;
    server_name _;

    client_max_body_size 10M;

    location /static/ {
        alias /static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /media/;
        expires 1d;
    }

    location /health/ {
        proxy_pass http://fintrack;
        access_log off;
    }

    location / {
        proxy_pass http://fintrack;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        # WebSocket support (untuk future use)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

### 17.3 Production Settings

Sudah didefinisikan di `config/settings/production.py` (lihat Fase 1.4).

---

### 17.4 CI/CD GitHub Actions

#### `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with:
          version: "latest"
      - run: uv sync --group dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: fintrack_test
          POSTGRES_USER: fintrack
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      redis:
        image: redis:7
        options: --health-cmd "redis-cli ping"
        ports:
          - 6379:6379

    env:
      DATABASE_URL: postgres://fintrack:testpass@localhost:5432/fintrack_test
      REDIS_URL: redis://localhost:6379/0
      DJANGO_SECRET_KEY: test-secret-key-for-ci
      DJANGO_SETTINGS_MODULE: config.settings.testing

    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --group dev
      - run: uv run python manage.py migrate
      - run: uv run pytest --cov --cov-report=xml -n auto
      - uses: codecov/codecov-action@v4
        if: always()
        with:
          file: ./coverage.xml

  docker-build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker images
        run: |
          docker build --target web -t fintrack-web .
          docker build --target worker -t fintrack-worker .
```

---

## FASE 18 — Monitoring

### 18.1 Sentry Integration

Sudah dikonfigurasi di `production.py`. Sentry otomatis menangkap:
- Django exceptions (views, middleware)
- Celery task failures
- Redis connection errors

---

### 18.2 Health Check Endpoint

`django-health-check` sudah dikonfigurasi di `INSTALLED_APPS` dan `urls.py`.

Akses di: `GET /health/`

Response contoh:

```json
{
  "DatabaseBackend": "working",
  "CacheBackend": "working",
  "DefaultFileStorageHealthCheck": "working",
  "CeleryHealthCheck": "working"
}
```

---

## Urutan Eksekusi (Quick Start)

Ikuti urutan ini untuk memulai dari nol:

```bash
# 1. Install semua dependencies
uv sync
uv add django-environ psycopg "psycopg[binary]" redis "celery[redis]" \
    django-celery-beat django-celery-results "django-allauth[socialaccount]" \
    django-htmx "django-storages[s3]" Pillow openpyxl reportlab \
    django-model-utils whitenoise django-csp django-ratelimit \
    "sentry-sdk[django]" django-health-check

# 2. Buat semua folder dan file
# (ikuti Fase 1.2)

# 3. Salin dan isi .env
cp .env.example .env

# 4. Inisialisasi Tailwind
uv run python manage.py tailwind init
uv run python manage.py tailwind install

# 5. Migrasi database
uv run python manage.py makemigrations
uv run python manage.py migrate

# 6. Buat superuser
uv run python manage.py createsuperuser

# 7. Download HTMX + Hyperscript
curl -L https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js -o static/js/htmx.min.js
curl -L https://unpkg.com/hyperscript.org@0.9.14/dist/_hyperscript.min.js -o static/js/hyperscript.min.js

# 8. Jalankan server
# Terminal 1:
uv run python manage.py runserver

# Terminal 2 (Tailwind hot reload):
uv run python manage.py tailwind start

# Terminal 3 (Celery — opsional untuk dev):
uv run celery -A config worker -l info

# 9. Akses aplikasi
# http://127.0.0.1:8000/dashboard/
# http://127.0.0.1:8000/admin/
```

---

## Catatan Penting & Perbedaan dari Docs Asli

| Item | Docs Asli | Implementasi Ini |
|---|---|---|
| Django version | 5.x | **6.0.4** (lebih baru, fully compatible) |
| Tailwind | Raw TailwindCSS v4 | **django-tailwind** (lebih mudah untuk Django) |
| Forms helper | crispy-forms | **django-widget-tweaks** (lebih fleksibel) |
| Cache session | `django_redis` | **Built-in Django Redis cache** (Django 4.2+) |
| Static storage | whitenoise | **whitenoise** (sama, tapi pakai STORAGES dict baru) |
| Background tasks | Celery + Redis | Celery tetap; **Django Background Tasks** optional |
| PostgreSQL | `psycopg[binary]` | Sama; SQLite untuk development |

---

*Dokumentasi ini mencakup 18 fase implementasi lengkap FinTrack.*
*Versi: 1.0.0 — Generated 2026-04-30*
