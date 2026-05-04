# FinTrack — Finance Tracking Application
### Comprehensive Technical Documentation

> **Stack:** `uv` · `Django 5.x` · `HTMX` · `Hyperscript` · `TailwindCSS v4` · `DaisyUI v5`
> **Philosophy:** Hypermedia-first, progressively enhanced, scalable by design.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Philosophy](#2-architecture-philosophy)
3. [Tech Stack Deep Dive](#3-tech-stack-deep-dive)
4. [Project Structure](#4-project-structure)
5. [Environment Setup](#5-environment-setup)
6. [Django Configuration](#6-django-configuration)
7. [Database Design](#7-database-design)
8. [Application Modules](#8-application-modules)
9. [URL Routing](#9-url-routing)
10. [Views & HTMX Patterns](#10-views--htmx-patterns)
11. [Template Architecture](#11-template-architecture)
12. [HTMX Integration Patterns](#12-htmx-integration-patterns)
13. [Hyperscript Patterns](#13-hyperscript-patterns)
14. [TailwindCSS + DaisyUI Conventions](#14-tailwindcss--daisyui-conventions)
15. [Forms & Validation](#15-forms--validation)
16. [Authentication & Authorization](#16-authentication--authorization)
17. [API Design (HTMX-first)](#17-api-design-htmx-first)
18. [Celery & Background Tasks](#18-celery--background-tasks)
19. [Caching Strategy](#19-caching-strategy)
20. [Testing Strategy](#20-testing-strategy)
21. [Security Checklist](#21-security-checklist)
22. [Performance Optimization](#22-performance-optimization)
23. [Deployment Guide](#23-deployment-guide)
24. [CI/CD Pipeline](#24-cicd-pipeline)
25. [Monitoring & Observability](#25-monitoring--observability)
26. [ADR Log](#26-adr-log)
27. [Glossary](#27-glossary)

---

## 1. Project Overview

**FinTrack** is a personal and team finance tracking web application that enables users to record, categorize, analyze, and visualize financial transactions. It is designed with a hypermedia-driven architecture (HTMX) to deliver a near-SPA experience without a heavy JavaScript framework.

### Core Features

| Feature | Description |
|---|---|
| Dashboard | Real-time KPI cards, income vs. expense chart, recent transactions |
| Transactions | Full CRUD, bulk import via CSV, smart categorization |
| Budgets | Monthly/weekly budget per category with progress tracking |
| Accounts | Multiple accounts (bank, wallet, credit card) with balance tracking |
| Reports | Date-range reports, category breakdown, export to CSV/PDF |
| Recurring | Automatic recurring transaction generation via Celery |
| Multi-currency | Base currency + live FX rate conversion |
| Auth | Registration, login, 2FA, OAuth (Google) |
| Team Mode | Shared household/team finance workspace |
| Notifications | In-app and email alerts (budget overage, large transactions) |

### Non-Functional Requirements

| Requirement | Target |
|---|---|
| Page load (TTFB) | < 200ms |
| HTMX partial response | < 100ms |
| Test coverage | ≥ 80% |
| Uptime SLA | 99.9% |
| Concurrent users | 10,000+ (horizontal scaling) |
| Mobile responsiveness | Full (DaisyUI responsive classes) |

---

## 2. Architecture Philosophy

### Hypermedia-First

FinTrack follows the **HATEOAS** (Hypermedia as the Engine of Application State) principle. Rather than building a REST/JSON API consumed by a JavaScript SPA, the server renders HTML fragments returned to HTMX-powered front-end interactions. This means:

- The server is the **single source of truth** for all state.
- JavaScript is used only for **progressive enhancement** (via Hyperscript and minimal vanilla JS).
- Every user interaction that requires data updates issues an **HTTP request** — HTMX handles swapping the resulting HTML into the DOM.

### Layered Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Browser / Client                  │
│        HTMX + Hyperscript + TailwindCSS/DaisyUI      │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP (full page or partial HTML)
┌──────────────────────▼──────────────────────────────┐
│                  Django Application                  │
│  Views → Forms → Services → Repositories → Models   │
└──────────────────────┬──────────────────────────────┘
                       │
         ┌─────────────┴──────────────┐
         │                            │
┌────────▼───────┐          ┌─────────▼──────┐
│  PostgreSQL DB │          │  Redis Cache   │
│  (primary data)│          │  + Celery MQ   │
└────────────────┘          └────────────────┘
```

### Design Patterns

| Pattern | Usage |
|---|---|
| **Service Layer** | Business logic isolated from views; `services/` module per app |
| **Repository Pattern** | DB query abstraction in `repositories/`; swappable for testing |
| **Template Partials** | HTML fragments served for HTMX swaps; reused in full pages |
| **Form Objects** | All input validated through Django Forms / ModelForms |
| **Signal-based Side Effects** | Email, notifications, audit log via Django signals |
| **Feature Flags** | Simple DB-backed flags for gradual rollout |

---

## 3. Tech Stack Deep Dive

### `uv` — Package & Environment Manager

`uv` is a blazing-fast Python package manager (written in Rust) that replaces `pip`, `pip-tools`, and `virtualenv` in one tool.

**Why uv:**
- 10–100× faster than pip for installs
- Built-in virtual environment management (`uv venv`)
- Lockfile (`uv.lock`) for deterministic builds — no more `requirements.txt` drift
- Compatible with `pyproject.toml` PEP 517/518 standard

### Django 6.x

Django 6.x brings:
- **`{% partial %}`** template tags (Django 6.x) for inline partial rendering
- Improved `async` view support (used for WebSocket-adjacent flows)
- `GeneratedField` for computed DB columns
- Facet filters in admin

### HTMX

HTMX allows any HTML element to issue HTTP requests and swap the result into the DOM declaratively via HTML attributes.

**Key concepts used in FinTrack:**
- `hx-get`, `hx-post`, `hx-put`, `hx-delete` — HTTP verbs
- `hx-target` — where to inject the response HTML
- `hx-swap` — how to inject (`innerHTML`, `outerHTML`, `beforeend`, `afterbegin`, etc.)
- `hx-trigger` — what triggers the request (`click`, `change`, `every 30s`, etc.)
- `hx-push-url` — update browser URL without full navigation
- `hx-boost` — progressive enhancement on anchor/form tags
- `hx-indicator` — show loading spinner during requests
- `hx-confirm` — native confirm dialog before destructive actions
- **Out-of-band swaps** (`hx-swap-oob`) — update multiple parts of page from one response

### Hyperscript

Hyperscript (`_="..."`) is a small, readable scripting language for UI behaviors that are too small to warrant Python roundtrips:

- Toggle CSS classes
- Show/hide elements
- Animate transitions
- Sync local UI state (e.g., live character counter)

### TailwindCSS v4

TailwindCSS v4 introduces a new CSS-first configuration system. No more `tailwind.config.js` — configuration lives in your CSS file using `@theme`.

### DaisyUI v5

DaisyUI provides semantic component classes (`btn`, `card`, `modal`, `badge`, `stat`, etc.) on top of Tailwind. It supports theming via CSS variables and includes 30+ built-in themes.

---

## 4. Project Structure

```
fintrack/
├── pyproject.toml               # Project metadata + dependencies
├── uv.lock                      # Deterministic lockfile (commit this)
├── .python-version              # Pinned Python version for uv
├── .env.example                 # Environment variable template
├── .env                         # Local secrets (gitignored)
├── manage.py
│
├── config/                      # Django project config (no business logic)
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py              # Shared settings
│   │   ├── development.py       # Dev overrides
│   │   ├── production.py        # Prod overrides
│   │   └── testing.py           # Test overrides
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py                  # For async support
│
├── apps/
│   ├── core/                    # Shared utilities, base models, middleware
│   │   ├── models.py            # TimeStampedModel, SoftDeleteModel, etc.
│   │   ├── middleware.py        # HTMX detection, timezone middleware
│   │   ├── mixins.py            # View mixins (HtmxMixin, etc.)
│   │   ├── templatetags/
│   │   │   ├── htmx_tags.py     # Custom HTMX template tags
│   │   │   └── finance_tags.py  # Currency, percentage formatters
│   │   └── utils/
│   │       ├── currency.py
│   │       └── dates.py
│   │
│   ├── accounts/                # User auth, profiles, teams
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── services/
│   │   │   └── auth_service.py
│   │   └── templates/accounts/
│   │
│   ├── finance/                 # Core finance domain
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── account.py       # FinancialAccount
│   │   │   ├── category.py      # Category, Subcategory
│   │   │   ├── transaction.py   # Transaction
│   │   │   ├── budget.py        # Budget, BudgetPeriod
│   │   │   └── recurring.py     # RecurringTransaction
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py
│   │   │   ├── transactions.py
│   │   │   ├── budgets.py
│   │   │   ├── accounts.py
│   │   │   └── reports.py
│   │   ├── forms/
│   │   │   ├── transaction_form.py
│   │   │   ├── budget_form.py
│   │   │   └── import_form.py
│   │   ├── services/
│   │   │   ├── transaction_service.py
│   │   │   ├── budget_service.py
│   │   │   ├── report_service.py
│   │   │   └── import_service.py
│   │   ├── repositories/
│   │   │   ├── transaction_repo.py
│   │   │   └── budget_repo.py
│   │   ├── tasks.py             # Celery tasks
│   │   ├── signals.py
│   │   ├── admin.py
│   │   ├── urls.py
│   │   └── templates/finance/
│   │       ├── dashboard.html
│   │       ├── transactions/
│   │       │   ├── list.html
│   │       │   ├── detail.html
│   │       │   ├── _form.html        # Partial
│   │       │   ├── _row.html         # Partial
│   │       │   └── _filters.html     # Partial
│   │       ├── budgets/
│   │       └── reports/
│   │
│   └── notifications/           # In-app & email notifications
│       ├── models.py
│       ├── services.py
│       ├── tasks.py
│       └── templates/notifications/
│
├── static/
│   ├── css/
│   │   └── app.css              # Tailwind @theme + @import + custom CSS
│   ├── js/
│   │   ├── htmx.min.js
│   │   ├── hyperscript.min.js
│   │   └── fintrack.js          # Minimal vanilla JS utilities
│   └── images/
│
├── templates/                   # Global templates
│   ├── base.html                # Root layout
│   ├── partials/
│   │   ├── _navbar.html
│   │   ├── _sidebar.html
│   │   ├── _toast.html          # OOB notification partial
│   │   ├── _breadcrumb.html
│   │   └── _pagination.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
├── locale/                      # i18n translations
├── tests/
│   ├── conftest.py
│   ├── factories/               # factory_boy factories
│   ├── unit/
│   ├── integration/
│   └── e2e/                     # Playwright tests
│
└── docker/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── docker-compose.prod.yml
    └── nginx/
        └── nginx.conf
```

---

## 5. Environment Setup

### Prerequisites

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify
uv --version  # uv 0.5.x or later
```

### Initialize Project

```bash
# Create project directory
mkdir fintrack && cd fintrack

# Initialize uv project (creates pyproject.toml)
uv init --python 3.12

# Create virtual environment
uv venv

# Activate (the uv way — or use `source .venv/bin/activate`)
# uv run <command>  automatically uses the venv
```

### `pyproject.toml`

```toml
[project]
name = "fintrack"
version = "0.1.0"
description = "Hypermedia-first personal finance tracker"
readme = "README.md"
requires-python = ">=3.12"

dependencies = [
    # Core
    "django>=6",
    "django-environ>=0.11",

    # Database
    "psycopg[binary]>=3.3",
    "django-db-geventpool>=4.0",

    # Cache & Task Queue
    "redis>=5.0",
    "celery[redis]>=5.4",
    "django-celery-beat>=2.7",
    "django-celery-results>=2.5",

    # Auth
    "django-allauth[socialaccount]>=65.0",
    "django-otp>=1.5",

    # Forms & Validation
    "django-crispy-forms>=2.3",
    "crispy-tailwind>=1.0",

    # HTMX helpers
    "django-htmx>=1.21",

    # Storage & Files
    "django-storages[s3]>=1.14",
    "Pillow>=11.0",

    # API & Serialization (for CSV/PDF export)
    "djangorestframework>=3.15",
    "openpyxl>=3.1",
    "reportlab>=4.2",

    # Utilities
    "django-model-utils>=5.0",
    "django-extensions>=3.2",
    "django-filter>=24.0",
    "django-money>=3.5",
    "py-moneyed>=3.0",

    # Security
    "django-csp>=4.0",
    "django-ratelimit>=4.1",

    # Monitoring
    "sentry-sdk[django]>=2.0",
    "django-health-check>=3.18",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-django>=4.9",
    "pytest-cov>=5.0",
    "pytest-xdist>=3.6",       # Parallel test execution
    "factory-boy>=3.3",
    "faker>=28.0",
    "playwright>=1.47",
    "pytest-playwright>=0.5",
    "django-debug-toolbar>=4.4",
    "ipython>=8.0",
    "pre-commit>=3.8",
    "ruff>=0.6",               # Linter + formatter
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
select = ["E", "F", "I", "N", "UP", "B", "S", "ANN"]
ignore = ["ANN101", "ANN102"]

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

### Install Dependencies

```bash
# Install all dependencies (uses uv.lock for reproducibility)
uv sync

# Install dev dependencies
uv sync --group dev

# Add a new package
uv add django-q2

# Remove a package
uv remove django-q2

# Upgrade all packages
uv lock --upgrade

# Run any command in the venv
uv run python manage.py runserver
uv run pytest
uv run celery -A config worker -l info
```

### Environment Variables (`.env`)

```bash
# Copy template
cp .env.example .env
```

**`.env.example`:**

```ini
# Django
DJANGO_SECRET_KEY=your-very-long-random-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=config.settings.development

# Database
DATABASE_URL=postgres://fintrack:password@localhost:5432/fintrack_db

# Cache & Queue
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@fintrack.app

# Storage (Production)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=ap-southeast-1

# OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# External APIs
EXCHANGERATE_API_KEY=

# Sentry
SENTRY_DSN=

# Security
DJANGO_SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

---

## 6. Django Configuration

### `config/settings/base.py`

```python
"""
Base settings — shared across all environments.
Never import this file directly; import a child settings file.
"""
from pathlib import Path
import environ

env = environ.Env(
    DEBUG=(bool, False),
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ─── Core ────────────────────────────────────────────────────────────────────
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost"])

# ─── Apps ────────────────────────────────────────────────────────────────────
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
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_htmx",
    "crispy_forms",
    "crispy_tailwind",
    "django_filters",
    "django_celery_beat",
    "django_celery_results",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.celery",
]

LOCAL_APPS = [
    "apps.core",
    "apps.accounts",
    "apps.finance",
    "apps.notifications",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ─── Middleware ───────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",      # Static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",           # Adds request.htmx
    "apps.core.middleware.TimezoneMiddleware",
    "apps.core.middleware.CurrentUserMiddleware",
]

ROOT_URLCONF = "config.urls"

# ─── Templates ───────────────────────────────────────────────────────────────
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

# ─── Database ────────────────────────────────────────────────────────────────
DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True   # Wrap every view in a transaction
DATABASES["default"]["CONN_MAX_AGE"] = 60

# ─── Cache ───────────────────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://localhost:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "fintrack",
        "TIMEOUT": 300,  # 5 minutes default
    }
}

# ─── Sessions ────────────────────────────────────────────────────────────────
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days
SESSION_COOKIE_HTTPONLY = True

# ─── Auth ────────────────────────────────────────────────────────────────────
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# ─── Allauth ─────────────────────────────────────────────────────────────────
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# ─── Celery ──────────────────────────────────────────────────────────────────
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/1")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="django-db")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes hard limit
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# ─── Static & Media ──────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ─── Internationalization ────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ─── Crispy Forms ────────────────────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# ─── Default PK ──────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── Logging ─────────────────────────────────────────────────────────────────
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

# ─── Finance App ─────────────────────────────────────────────────────────────
FINTRACK_BASE_CURRENCY = "IDR"
FINTRACK_SUPPORTED_CURRENCIES = ["IDR", "USD", "EUR", "SGD", "JPY"]
FINTRACK_EXCHANGE_RATE_REFRESH_HOURS = 6
```

---

## 7. Database Design

### Entity-Relationship Overview

```
User ──< Team >── TeamMember
  │
  ├──< FinancialAccount
  │       │
  │       └──< Transaction >── Category >── Subcategory
  │                │
  │                └── Tag (M2M)
  │
  ├──< Budget
  │       │
  │       └── BudgetPeriod >── Category
  │
  └──< RecurringTransaction
```

### Core Models

#### `apps/core/models.py` — Abstract Base Models

```python
import uuid
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base: created_at + updated_at on every model."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base: UUID primary key."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    """Abstract base: soft delete instead of hard delete."""
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Includes soft-deleted

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
    """Combine all abstract bases — use this for most domain models."""
    class Meta:
        abstract = True
```

#### `apps/accounts/models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """Extended user model."""
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


class Team(TimeStampedModel):
    """Shared workspace for household/family finance tracking."""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_teams")
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "accounts_team"


class TeamMembership(TimeStampedModel):
    ROLE_VIEWER = "viewer"
    ROLE_EDITOR = "editor"
    ROLE_ADMIN = "admin"
    ROLES = [
        (ROLE_VIEWER, "Viewer"),
        (ROLE_EDITOR, "Editor"),
        (ROLE_ADMIN, "Admin"),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=10, choices=ROLES, default=ROLE_VIEWER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts_team_membership"
        unique_together = [("team", "user")]
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="financial_accounts")
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    currency = models.CharField(max_length=3, default="IDR")
    initial_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    color = models.CharField(max_length=7, default="#3B82F6")  # Hex color
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
        null=True, blank=True,  # Null = system default category
    )
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    icon = models.CharField(max_length=50, default="tag")
    color = models.CharField(max_length=7, default="#6B7280")
    is_system = models.BooleanField(default=False)  # Built-in categories
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(
        FinancialAccount, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="transactions"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="transactions")

    # Transfer-specific
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
    # Amount converted to user's base currency
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
    receipt_image = models.ImageField(upload_to="receipts/%Y/%m/", blank=True, null=True)
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

---

## 8. Application Modules

### `apps/finance/services/transaction_service.py`

The service layer contains all business logic. Views should never directly query the database — they delegate to services.

```python
from decimal import Decimal
from typing import Optional
from datetime import date

from django.db import transaction as db_transaction
from django.contrib.auth import get_user_model

from apps.finance.models import Transaction, FinancialAccount, Category
from apps.finance.repositories.transaction_repo import TransactionRepository
from apps.notifications.services import NotificationService

User = get_user_model()


class TransactionService:
    def __init__(
        self,
        repo: Optional[TransactionRepository] = None,
        notification_service: Optional[NotificationService] = None,
    ):
        self.repo = repo or TransactionRepository()
        self.notification_service = notification_service or NotificationService()

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
        """Create a transaction and update account balance."""
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
        """Update a transaction, reversing old balance impact."""
        old_amount = txn.amount
        old_type = txn.transaction_type

        updated = self.repo.update(txn, **fields)

        # Reverse old impact, apply new impact
        self._reverse_account_balance(txn.account, old_amount, old_type)
        self._update_account_balance(updated.account, updated)
        return updated

    @db_transaction.atomic
    def delete_transaction(self, txn: Transaction) -> None:
        """Soft-delete and reverse the account balance."""
        self._reverse_account_balance(txn.account, txn.amount, txn.transaction_type)
        txn.delete()  # Soft delete via SoftDeleteModel

    def _update_account_balance(self, account: FinancialAccount, txn: Transaction) -> None:
        if txn.transaction_type == Transaction.TYPE_INCOME:
            account.current_balance += txn.amount
        elif txn.transaction_type == Transaction.TYPE_EXPENSE:
            account.current_balance -= txn.amount
        account.save(update_fields=["current_balance"])

    def _reverse_account_balance(self, account: FinancialAccount, amount: Decimal, txn_type: str) -> None:
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

### `apps/finance/repositories/transaction_repo.py`

```python
from typing import Optional
from django.db.models import QuerySet, Sum, Q
from datetime import date

from apps.finance.models import Transaction


class TransactionRepository:
    """Encapsulates all DB queries for Transaction model."""

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
                Q(description__icontains=search) |
                Q(payee__icontains=search) |
                Q(notes__icontains=search)
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
        result["total_income"] = result["total_income"] or 0
        result["total_expense"] = result["total_expense"] or 0
        result["net"] = result["total_income"] - result["total_expense"]
        return result

    def create(self, **kwargs) -> Transaction:
        return Transaction.objects.create(**kwargs)

    def update(self, txn: Transaction, **fields) -> Transaction:
        for attr, value in fields.items():
            setattr(txn, attr, value)
        txn.save()
        return txn
```

---

## 9. URL Routing

### `config/urls.py`

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

### `apps/finance/urls.py`

```python
from django.urls import path
from apps.finance.views import dashboard, transactions, budgets, accounts, reports

app_name = "finance"

urlpatterns = [
    # Dashboard
    path("dashboard/", dashboard.DashboardView.as_view(), name="dashboard"),
    path("dashboard/summary/", dashboard.DashboardSummaryView.as_view(), name="dashboard-summary"),

    # Transactions
    path("transactions/", transactions.TransactionListView.as_view(), name="transaction-list"),
    path("transactions/create/", transactions.TransactionCreateView.as_view(), name="transaction-create"),
    path("transactions/<uuid:pk>/", transactions.TransactionDetailView.as_view(), name="transaction-detail"),
    path("transactions/<uuid:pk>/edit/", transactions.TransactionUpdateView.as_view(), name="transaction-update"),
    path("transactions/<uuid:pk>/delete/", transactions.TransactionDeleteView.as_view(), name="transaction-delete"),
    path("transactions/import/", transactions.TransactionImportView.as_view(), name="transaction-import"),
    path("transactions/export/", transactions.TransactionExportView.as_view(), name="transaction-export"),

    # Partial endpoints (HTMX only)
    path("transactions/filter/", transactions.TransactionFilterView.as_view(), name="transaction-filter"),
    path("transactions/<uuid:pk>/row/", transactions.TransactionRowView.as_view(), name="transaction-row"),

    # Budgets
    path("budgets/", budgets.BudgetListView.as_view(), name="budget-list"),
    path("budgets/create/", budgets.BudgetCreateView.as_view(), name="budget-create"),
    path("budgets/<uuid:pk>/edit/", budgets.BudgetUpdateView.as_view(), name="budget-update"),
    path("budgets/<uuid:pk>/delete/", budgets.BudgetDeleteView.as_view(), name="budget-delete"),

    # Accounts
    path("accounts-list/", accounts.AccountListView.as_view(), name="account-list"),
    path("accounts/create/", accounts.AccountCreateView.as_view(), name="account-create"),
    path("accounts/<uuid:pk>/", accounts.AccountDetailView.as_view(), name="account-detail"),

    # Reports
    path("reports/", reports.ReportView.as_view(), name="reports"),
    path("reports/data/", reports.ReportDataView.as_view(), name="reports-data"),
]
```

---

## 10. Views & HTMX Patterns

### `apps/core/mixins.py`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django_htmx.http import HttpResponseClientRedirect


class HtmxMixin:
    """
    Mixin for views that respond to both HTMX and regular requests.
    """
    htmx_template: str = ""      # Template for HTMX partial response
    full_template: str = ""       # Template for full page response

    def get_template_names(self):
        if self.request.htmx and self.htmx_template:
            return [self.htmx_template]
        return [self.full_template or super().get_template_names()[0]]

    def htmx_redirect(self, url: str):
        """Redirect that works correctly inside HTMX requests."""
        if self.request.htmx:
            return HttpResponseClientRedirect(url)
        from django.shortcuts import redirect
        return redirect(url)


class OwnershipMixin:
    """Ensures users can only access their own objects."""
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class FinanceViewMixin(LoginRequiredMixin, OwnershipMixin, HtmxMixin):
    """Base mixin for all finance views."""
    pass
```

### `apps/finance/views/transactions.py`

```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django_htmx.http import trigger_client_event, HttpResponseClientRefresh

from apps.core.mixins import FinanceViewMixin
from apps.finance.models import Transaction
from apps.finance.forms import TransactionForm
from apps.finance.services.transaction_service import TransactionService
from apps.finance.repositories.transaction_repo import TransactionRepository


class TransactionListView(FinanceViewMixin, ListView):
    model = Transaction
    full_template = "finance/transactions/list.html"
    htmx_template = "finance/transactions/_list_partial.html"
    context_object_name = "transactions"
    paginate_by = 25

    def get_queryset(self):
        repo = TransactionRepository()
        return repo.get_user_transactions(
            user=self.request.user,
            start_date=self.request.GET.get("start_date"),
            end_date=self.request.GET.get("end_date"),
            category_id=self.request.GET.get("category"),
            account_id=self.request.GET.get("account"),
            transaction_type=self.request.GET.get("type"),
            search=self.request.GET.get("q"),
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filters"] = self.request.GET
        return ctx


class TransactionCreateView(FinanceViewMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    full_template = "finance/transactions/create.html"
    htmx_template = "finance/transactions/_form.html"
    success_url = reverse_lazy("finance:transaction-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        service = TransactionService()
        data = form.cleaned_data
        txn = service.create_transaction(
            user=self.request.user,
            account=data["account"],
            category=data.get("category"),
            transaction_type=data["transaction_type"],
            amount=data["amount"],
            date=data["date"],
            description=data["description"],
            **{k: v for k, v in data.items() if k not in [
                "account", "category", "transaction_type", "amount", "date", "description"
            ]},
        )
        messages.success(self.request, "Transaction added successfully.")

        if self.request.htmx:
            response = HttpResponse(status=204)
            trigger_client_event(response, "transactionAdded", {})
            return response
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.htmx:
            return self.render_to_response(self.get_context_data(form=form), status=422)
        return super().form_invalid(form)


class TransactionDeleteView(FinanceViewMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy("finance:transaction-list")

    def delete(self, request, *args, **kwargs):
        txn = self.get_object()
        service = TransactionService()
        service.delete_transaction(txn)
        messages.success(request, "Transaction deleted.")

        if request.htmx:
            response = HttpResponse(status=200)
            trigger_client_event(response, "transactionDeleted", {"id": str(txn.id)})
            return response
        return super().delete(request, *args, **kwargs)


class TransactionRowView(FinanceViewMixin, DetailView):
    """Return a single transaction row partial (used after inline edit)."""
    model = Transaction
    template_name = "finance/transactions/_row.html"


class TransactionFilterView(FinanceViewMixin, ListView):
    """HTMX-only: returns filtered transaction list partial."""
    model = Transaction
    template_name = "finance/transactions/_list_partial.html"
    context_object_name = "transactions"
    paginate_by = 25

    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest("HTMX only")
        return super().dispatch(request, *args, **kwargs)
```

---

## 11. Template Architecture

### `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en" data-theme="fintrack" class="h-full">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{% block title %}FinTrack{% endblock %}</title>

  {# TailwindCSS + DaisyUI — CDN for dev; compiled for prod #}
  {% if debug %}
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5/dist/full.min.css" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com"></script>
  {% else %}
    <link rel="stylesheet" href="{% static 'css/app.css' %}" />
  {% endif %}

  {# HTMX + Hyperscript #}
  <script src="{% static 'js/htmx.min.js' %}" defer></script>
  <script src="{% static 'js/hyperscript.min.js' %}" defer></script>

  {# HTMX config #}
  <meta name="htmx-config" content='{"globalViewTransitions": true, "defaultSwapStyle": "innerHTML"}' />

  {# CSRF for HTMX #}
  <meta name="csrf-token" content="{{ csrf_token }}" />

  {% block extra_head %}{% endblock %}
</head>

<body
  class="h-full bg-base-200"
  hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
>

  {# Toast notification container — updated via OOB swaps #}
  <div id="toast-container" class="toast toast-top toast-end z-50">
    {% include "partials/_toast.html" %}
  </div>

  {# App Shell #}
  {% if user.is_authenticated %}
    <div class="flex h-full">
      {% include "partials/_sidebar.html" %}

      <div class="flex-1 flex flex-col overflow-hidden">
        {% include "partials/_navbar.html" %}

        <main id="main-content" class="flex-1 overflow-y-auto p-6">
          {% block content %}{% endblock %}
        </main>
      </div>
    </div>
  {% else %}
    {% block auth_content %}{% endblock %}
  {% endif %}

  {# Django messages → HTMX toast OOB #}
  {% if messages %}
    {% for message in messages %}
      <div
        id="toast-container"
        hx-swap-oob="beforeend"
      >
        <div class="alert alert-{{ message.tags }} shadow-lg mb-2"
             _="on load wait 4s then add .opacity-0 transition-opacity duration-500 then wait 500ms then remove me">
          <span>{{ message }}</span>
        </div>
      </div>
    {% endfor %}
  {% endif %}

  {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### `templates/finance/transactions/list.html`

```html
{% extends "base.html" %}
{% load finance_tags %}

{% block title %}Transactions — FinTrack{% endblock %}

{% block content %}
<div class="space-y-6">
  {# Page Header #}
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-2xl font-bold text-base-content">Transactions</h1>
      <p class="text-base-content/60 text-sm">Track your income and expenses</p>
    </div>
    <button
      class="btn btn-primary gap-2"
      hx-get="{% url 'finance:transaction-create' %}"
      hx-target="#modal-container"
      hx-swap="innerHTML"
      _="on htmx:afterSwap call document.getElementById('txn-modal').showModal()"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
      </svg>
      Add Transaction
    </button>
  </div>

  {# Filters Panel #}
  <div class="card bg-base-100 shadow-sm">
    <div class="card-body py-4">
      <form
        hx-get="{% url 'finance:transaction-filter' %}"
        hx-target="#transaction-list"
        hx-swap="innerHTML"
        hx-trigger="change from:select, input from:input[type=date] delay:300ms, keyup from:input[type=search] delay:400ms"
        hx-push-url="true"
      >
        {% include "finance/transactions/_filters.html" %}
      </form>
    </div>
  </div>

  {# Transaction List — swapped by HTMX filters #}
  <div id="transaction-list">
    {% include "finance/transactions/_list_partial.html" %}
  </div>
</div>

{# Modal container for create/edit forms #}
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
  // Refresh list when transaction is added/deleted
  htmx.on("transactionAdded", () => {
    document.getElementById("txn-modal").close();
    htmx.trigger("#transaction-list", "refresh");
  });
  htmx.on("transactionDeleted", (evt) => {
    const row = document.getElementById(`txn-row-${evt.detail.id}`);
    if (row) {
      row.classList.add("opacity-0", "transition-opacity");
      setTimeout(() => row.remove(), 300);
    }
  });
</script>
{% endblock %}
```

### `templates/finance/transactions/_row.html`

```html
<tr
  id="txn-row-{{ transaction.id }}"
  class="hover:bg-base-200 transition-colors"
>
  <td class="w-10">
    <input type="checkbox" class="checkbox checkbox-sm" name="txn-ids" value="{{ transaction.id }}" />
  </td>
  <td>
    <span class="text-sm text-base-content/60">{{ transaction.date|date:"d M Y" }}</span>
  </td>
  <td>
    <div class="flex items-center gap-3">
      <div
        class="badge badge-sm"
        style="background-color: {{ transaction.category.color }}20; color: {{ transaction.category.color }};"
      >
        {{ transaction.category.icon }} {{ transaction.category.name|default:"—" }}
      </div>
    </div>
  </td>
  <td class="max-w-xs truncate">
    {{ transaction.description }}
    {% if transaction.payee %}
      <span class="text-base-content/50 text-xs ml-1">· {{ transaction.payee }}</span>
    {% endif %}
  </td>
  <td>
    <span class="badge badge-outline badge-sm">{{ transaction.account.name }}</span>
  </td>
  <td class="text-right font-mono font-semibold {% if transaction.is_income %}text-success{% else %}text-error{% endif %}">
    {% if transaction.is_income %}+{% else %}-{% endif %}
    {{ transaction.amount|currency:transaction.currency }}
  </td>
  <td>
    <div class="flex gap-1 justify-end">
      <button
        class="btn btn-ghost btn-xs"
        hx-get="{% url 'finance:transaction-update' transaction.pk %}"
        hx-target="#modal-container"
        hx-swap="innerHTML"
        _="on htmx:afterSwap call document.getElementById('txn-modal').showModal()"
        title="Edit"
      >
        ✏️
      </button>
      <button
        class="btn btn-ghost btn-xs text-error"
        hx-delete="{% url 'finance:transaction-delete' transaction.pk %}"
        hx-confirm="Delete this transaction? This cannot be undone."
        hx-target="closest tr"
        hx-swap="outerHTML swap:500ms"
        title="Delete"
      >
        🗑️
      </button>
    </div>
  </td>
</tr>
```

---

## 12. HTMX Integration Patterns

### Pattern 1: Infinite Scroll

```html
{# Last item in a list triggers loading next page #}
{% if page_obj.has_next %}
<tr
  hx-get="?page={{ page_obj.next_page_number }}&{{ request.GET.urlencode }}"
  hx-trigger="intersect once"
  hx-target="this"
  hx-swap="afterend"
>
  <td colspan="7" class="text-center py-4">
    <span class="loading loading-spinner loading-sm"></span>
  </td>
</tr>
{% endif %}
```

### Pattern 2: Inline Edit (Click to Edit)

```html
{# Display mode #}
<span
  id="budget-amount-{{ budget.pk }}"
  class="cursor-pointer hover:text-primary"
  hx-get="{% url 'finance:budget-update' budget.pk %}?field=amount"
  hx-target="this"
  hx-swap="outerHTML"
>
  {{ budget.amount|currency:budget.currency }}
</span>

{# Edit mode (returned by server) #}
<form
  hx-patch="{% url 'finance:budget-update' budget.pk %}"
  hx-target="#budget-amount-{{ budget.pk }}"
  hx-swap="outerHTML"
>
  <input
    name="amount"
    type="number"
    value="{{ budget.amount }}"
    class="input input-bordered input-sm w-32"
    autofocus
    _="on keyup[key=='Escape'] send cancel to me"
  />
  <button type="submit" class="btn btn-primary btn-xs">Save</button>
  <button
    type="button"
    class="btn btn-ghost btn-xs"
    hx-get="{% url 'finance:budget-row' budget.pk %}"
    hx-target="#budget-amount-{{ budget.pk }}"
    hx-swap="outerHTML"
  >
    Cancel
  </button>
</form>
```

### Pattern 3: Out-of-Band (OOB) Updates

When creating a transaction, we need to update: the transaction list, the account balance widget, and the toast notification — all from a single POST response.

```python
# views.py — return multiple HTML fragments
def form_valid(self, form):
    txn = service.create_transaction(...)

    if self.request.htmx:
        # Render multiple partials and combine them
        from django.template.loader import render_to_string

        new_row_html = render_to_string(
            "finance/transactions/_row.html",
            {"transaction": txn},
            request=self.request,
        )
        account_balance_html = render_to_string(
            "finance/accounts/_balance_widget.html",
            {"account": txn.account},
            request=self.request,
        )
        toast_html = render_to_string(
            "partials/_toast_item.html",
            {"message": "Transaction added!", "level": "success"},
        )

        # Combine with OOB swap attributes baked in
        combined = f"""
          {new_row_html}
          <div id="account-balance-{txn.account.pk}" hx-swap-oob="true">
            {account_balance_html}
          </div>
          <div id="toast-container" hx-swap-oob="beforeend">
            {toast_html}
          </div>
        """
        return HttpResponse(combined)
```

### Pattern 4: Polling (Live Dashboard)

```html
{# Auto-refresh KPI cards every 60 seconds #}
<div
  id="kpi-cards"
  hx-get="{% url 'finance:dashboard-summary' %}"
  hx-trigger="every 60s"
  hx-swap="innerHTML"
>
  {% include "finance/dashboard/_kpi_cards.html" %}
</div>
```

### Pattern 5: Search with Debounce

```html
<input
  type="search"
  name="q"
  placeholder="Search transactions..."
  class="input input-bordered w-full max-w-sm"
  hx-get="{% url 'finance:transaction-filter' %}"
  hx-trigger="keyup changed delay:400ms, search"
  hx-target="#transaction-list"
  hx-swap="innerHTML"
  hx-push-url="true"
  hx-indicator="#search-spinner"
/>
<span id="search-spinner" class="htmx-indicator loading loading-spinner loading-sm"></span>
```

### Pattern 6: Confirmation Dialog (Progressive Enhancement)

```html
{# DaisyUI modal + HTMX for delete confirmation #}
<button
  class="btn btn-error btn-sm"
  _="on click
     set #confirm-msg.textContent to 'Delete &quot;{{ transaction.description }}&quot;?'
     call #delete-confirm-modal.showModal()
     set #confirm-delete-btn's hx-delete to '{% url 'finance:transaction-delete' transaction.pk %}'
     then htmx.process(#confirm-delete-btn)"
>
  Delete
</button>

<dialog id="delete-confirm-modal" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg text-error">Confirm Delete</h3>
    <p id="confirm-msg" class="py-4"></p>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn btn-ghost">Cancel</button>
      </form>
      <button
        id="confirm-delete-btn"
        class="btn btn-error"
        hx-target="closest tr"
        hx-swap="outerHTML swap:500ms"
        _="on click call #delete-confirm-modal.close()"
      >
        Delete
      </button>
    </div>
  </div>
</dialog>
```

---

## 13. Hyperscript Patterns

### Toggle Theme

```html
<button
  class="btn btn-ghost btn-circle"
  _="on click
     if document.documentElement.getAttribute('data-theme') == 'fintrack'
       set document.documentElement's *data-theme to 'dark'
     else
       set document.documentElement's *data-theme to 'fintrack'
     end
     localStorage.setItem('theme', document.documentElement.getAttribute('data-theme'))"
>
  🌙
</button>
```

### Live Character Counter

```html
<textarea
  name="notes"
  class="textarea textarea-bordered w-full"
  maxlength="500"
  _="on keyup put (500 - my.value.length) + ' chars left' into #char-count.textContent"
></textarea>
<span id="char-count" class="text-xs text-base-content/50">500 chars left</span>
```

### Copy to Clipboard

```html
<button
  class="btn btn-ghost btn-xs"
  _="on click
     writeText(#account-number.textContent) to navigator.clipboard
     set my.textContent to 'Copied!'
     wait 2s
     set my.textContent to 'Copy'"
>
  Copy
</button>
```

### Sticky Header on Scroll

```html
<nav
  class="navbar bg-base-100"
  _="on scroll from window
       if window.scrollY > 10
         add .shadow-md to me
       else
         remove .shadow-md from me
       end"
>
```

### Auto-dismiss Toast

```html
{# In _toast_item.html #}
<div
  class="alert alert-success shadow-lg mb-2 transition-all duration-500"
  _="on load
       wait 3.5s
       add .opacity-0 .translate-x-full
       wait 500ms
       remove me"
>
  <span>{{ message }}</span>
</div>
```

---

## 14. TailwindCSS + DaisyUI Conventions

### `static/css/app.css`

```css
/* TailwindCSS v4 — CSS-first configuration */
@import "tailwindcss";
@import "daisyui" layer(components);

@source "../templates/**/*.html";
@source "../apps/**/*.html";
@source "../static/js/*.js";

/* ─── Custom FinTrack Theme ─────────────────────────────────────────────── */
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

/* ─── Custom Utilities ────────────────────────────────────────────────────── */
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

/* ─── HTMX Loading Indicator ─────────────────────────────────────────────── */
.htmx-indicator {
  opacity: 0;
  transition: opacity 200ms ease-in;
}
.htmx-request .htmx-indicator,
.htmx-request.htmx-indicator {
  opacity: 1;
}

/* ─── View Transitions ────────────────────────────────────────────────────── */
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

### DaisyUI Component Conventions

| Component | Usage in FinTrack |
|---|---|
| `card` | Dashboard KPI blocks, account cards, budget cards |
| `stat` | Dashboard summary numbers (total income, expense, net) |
| `table` | Transaction list, budget list |
| `modal` | Create/edit forms, delete confirmation |
| `badge` | Category chips, transaction type labels, status indicators |
| `progress` | Budget utilization bars |
| `alert` | Toast notifications, validation errors |
| `drawer` | Mobile sidebar navigation |
| `tabs` | Report views (monthly, yearly, category) |
| `select`, `input`, `textarea` | All form fields |
| `btn` | All actions (primary/ghost/error variants) |

---

## 15. Forms & Validation

### `apps/finance/forms/transaction_form.py`

```python
from django import forms
from django.contrib.auth import get_user_model
from apps.finance.models import Transaction, FinancialAccount, Category

User = get_user_model()


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "transaction_type", "account", "category",
            "amount", "date", "description", "payee",
            "notes", "tags", "status", "reference_number",
        ]
        widgets = {
            "transaction_type": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "account": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "category": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "amount": forms.NumberInput(attrs={
                "class": "input input-bordered w-full",
                "step": "0.01",
                "min": "0.01",
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
            "status": forms.Select(attrs={"class": "select select-bordered w-full"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Scope accounts and categories to the current user
            self.fields["account"].queryset = FinancialAccount.objects.filter(
                user=user, is_active=True
            )
            self.fields["category"].queryset = Category.objects.filter(
                models.Q(user=user) | models.Q(is_system=True)
            )

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned = super().clean()
        txn_type = cleaned.get("transaction_type")
        category = cleaned.get("category")

        if category and txn_type and category.category_type != txn_type:
            self.add_error(
                "category",
                f"Category type '{category.category_type}' doesn't match "
                f"transaction type '{txn_type}'."
            )
        return cleaned
```

---

## 16. Authentication & Authorization

### Custom User + Allauth Setup

```python
# apps/accounts/views.py

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from .models import User
from .forms import UserProfileForm


@method_decorator(login_required, name="dispatch")
class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile.html"

    def get_object(self):
        return self.request.user
```

### Object-Level Permissions

```python
# apps/core/permissions.py

from django.core.exceptions import PermissionDenied


def assert_owns(user, obj) -> None:
    """Raise PermissionDenied if user does not own obj."""
    if hasattr(obj, "user") and obj.user != user:
        raise PermissionDenied
    if hasattr(obj, "team") and not obj.team.memberships.filter(user=user).exists():
        raise PermissionDenied
```

---

## 17. API Design (HTMX-first)

FinTrack uses **HTML-over-the-wire** as its primary API. However, a minimal JSON API is exposed for:
- Mobile clients (future)
- CSV/PDF export
- Webhook integration

### Response Content Negotiation

```python
# apps/core/mixins.py

class HtmxOrJsonMixin:
    """
    Respond with HTML partial for HTMX, JSON for API clients.
    """
    def render_htmx_or_json(self, data: dict, template: str, status: int = 200):
        if self.request.htmx:
            return render(self.request, template, data, status=status)
        return JsonResponse(data, status=status)
```

### HTMX Request Detection

```python
# django-htmx adds request.htmx — a truthy object with HTMX headers
# Access it in any view:

def my_view(request):
    if request.htmx:
        # Partial response
        return render(request, "partials/_something.html", context)

    # Full page response
    return render(request, "full_page.html", context)
```

---

## 18. Celery & Background Tasks

### `config/celery.py`

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

### `apps/finance/tasks.py`

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
    """
    Runs daily (via Celery Beat) to create transaction instances
    from active RecurringTransaction templates.
    """
    from apps.finance.models import RecurringTransaction
    from apps.finance.services.transaction_service import TransactionService

    today = timezone.localdate()
    service = TransactionService()
    generated_count = 0

    due = RecurringTransaction.objects.filter(
        is_active=True,
        next_due_date__lte=today,
    ).select_related("user", "account", "category")

    for recurring in due:
        try:
            service.create_from_recurring(recurring, date=today)
            recurring.advance_next_due_date()
            generated_count += 1
        except Exception as exc:
            logger.error(
                f"Failed to generate recurring transaction {recurring.pk}: {exc}"
            )

    logger.info(f"Generated {generated_count} recurring transactions for {today}")
    return generated_count


@shared_task(name="finance.refresh_exchange_rates")
def refresh_exchange_rates():
    """Refresh FX rates from external API."""
    from apps.finance.services.currency_service import CurrencyService
    CurrencyService().refresh_all_rates()


@shared_task(name="finance.send_budget_alert")
def send_budget_alert(budget_id: str, user_id: int, percentage: float):
    """Send budget overage notification."""
    from apps.finance.models import Budget
    from apps.notifications.services import NotificationService

    budget = Budget.objects.select_related("user", "category").get(pk=budget_id)
    NotificationService().send_budget_alert(budget, percentage)
```

### Celery Beat Schedule

```python
# In Django Admin → Periodic Tasks, or define in settings:

CELERY_BEAT_SCHEDULE = {
    "generate-recurring-transactions": {
        "task": "finance.generate_recurring_transactions",
        "schedule": "0 1 * * *",  # Daily at 01:00 UTC
    },
    "refresh-exchange-rates": {
        "task": "finance.refresh_exchange_rates",
        "schedule": "0 */6 * * *",  # Every 6 hours
    },
}
```

---

## 19. Caching Strategy

### Cache Layers

| Layer | What | TTL | Tool |
|---|---|---|---|
| View-level | Dashboard summary HTML | 5 min | `cache_page` |
| Query-level | Monthly aggregates | 10 min | `cache.get/set` |
| Template fragment | Category list dropdown | 1 hour | `{% cache %}` |
| HTTP | Static assets | 1 year | WhiteNoise |

### Example

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 5, key_prefix="dashboard"), name="dispatch")
class DashboardSummaryView(LoginRequiredMixin, TemplateView):
    template_name = "finance/dashboard/_kpi_cards.html"
```

```html
{# Template fragment cache — category dropdown #}
{% load cache %}
{% cache 3600 "category-dropdown" request.user.pk %}
  <select name="category" class="select select-bordered">
    {% for cat in categories %}
      <option value="{{ cat.pk }}">{{ cat.name }}</option>
    {% endfor %}
  </select>
{% endcache %}
```

---

## 20. Testing Strategy

### `tests/conftest.py`

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

### `tests/factories/__init__.py`

```python
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from apps.finance.models import Transaction, FinancialAccount, Category

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_onboarded = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class FinancialAccountFactory(DjangoModelFactory):
    class Meta:
        model = FinancialAccount

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("company")
    account_type = FinancialAccount.TYPE_BANK
    currency = "IDR"
    initial_balance = factory.Faker("pydecimal", left_digits=8, right_digits=2, positive=True)
    current_balance = factory.LazyAttribute(lambda o: o.initial_balance)


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    account = factory.SubFactory(FinancialAccountFactory, user=factory.SelfAttribute("..user"))
    transaction_type = Transaction.TYPE_EXPENSE
    amount = factory.Faker("pydecimal", left_digits=6, right_digits=2, positive=True)
    currency = "IDR"
    date = factory.Faker("date_this_year")
    description = factory.Faker("sentence", nb_words=4)
```

### Sample Unit Test

```python
# tests/unit/test_transaction_service.py

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
        assert account.current_balance == balance_before + transaction.amount
```

### HTMX Integration Test

```python
# tests/integration/test_transaction_views.py

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestTransactionCreateView:
    def test_htmx_create_returns_204(self, auth_client, account):
        url = reverse("finance:transaction-create")
        response = auth_client.post(
            url,
            data={
                "transaction_type": "expense",
                "account": str(account.pk),
                "amount": "50000",
                "date": "2026-04-30",
                "description": "Lunch",
            },
            headers={"HX-Request": "true"},
        )
        assert response.status_code == 204
        assert "HX-Trigger" in response.headers

    def test_htmx_create_invalid_returns_422(self, auth_client, account):
        url = reverse("finance:transaction-create")
        response = auth_client.post(
            url,
            data={"amount": "-100"},  # Invalid
            headers={"HX-Request": "true"},
        )
        assert response.status_code == 422
```

---

## 21. Security Checklist

### Django Security Settings (Production)

```python
# config/settings/production.py

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
REFERRER_POLICY = "strict-origin-when-cross-origin"

# Content Security Policy (django-csp)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")  # Needed for HTMX inline handlers
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")    # Needed for Tailwind inline styles
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'",)
```

### HTMX Security

```html
{# Always set CSRF header for HTMX requests #}
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>

{# Validate HTMX origin in middleware #}
```

```python
# apps/core/middleware.py

class HtmxSecurityMiddleware:
    """Ensure HTMX requests originate from the same host."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.htmx:
            current_url = request.META.get("HTTP_HX_CURRENT_URL", "")
            if current_url and not current_url.startswith(
                f"https://{request.get_host()}"
            ):
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("Invalid HTMX origin")
        return self.get_response(request)
```

### Rate Limiting

```python
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key="user", rate="100/m", method="POST"), name="dispatch")
class TransactionCreateView(FinanceViewMixin, CreateView):
    ...
```

---

## 22. Performance Optimization

### QuerySet Optimization Checklist

```python
# ✅ Always select_related for FKs accessed in templates
Transaction.objects.select_related("account", "category", "user")

# ✅ Always prefetch_related for M2M
Transaction.objects.prefetch_related("tags")

# ✅ Use only() to limit columns for list views
Transaction.objects.only("id", "date", "description", "amount", "currency", "transaction_type")

# ✅ Use values() for aggregation
Transaction.objects.filter(user=user).values("category__name").annotate(total=Sum("amount"))

# ✅ Use iterator() for large exports
for txn in Transaction.objects.filter(user=user).iterator(chunk_size=1000):
    writer.writerow(...)

# ✅ Avoid N+1 with django-debug-toolbar in development
```

### Database Indexes

```python
class Transaction(BaseModel):
    class Meta:
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "category"]),
            models.Index(fields=["user", "transaction_type", "date"]),
            models.Index(fields=["account", "date"]),
            models.Index(
                fields=["user", "deleted_at"],
                condition=models.Q(deleted_at__isnull=True),
                name="active_transactions_idx",
            ),
        ]
```

### HTMX Performance

- Use `hx-boost="true"` on the `<body>` or `<a>` tags to convert regular navigation to partial swaps
- Serve HTMX from CDN with long-term caching
- Use `hx-swap="outerHTML"` to minimize DOM operations
- Leverage View Transitions API for smooth swaps

---

## 23. Deployment Guide

### Docker Setup

**`docker/Dockerfile`**

```dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application
COPY . .

# Collect static files
RUN uv run python manage.py collectstatic --noinput

FROM base AS web
EXPOSE 8000
CMD ["uv", "run", "gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "gthread", \
     "--threads", "2", \
     "--timeout", "120", \
     "--access-logfile", "-"]

FROM base AS worker
CMD ["uv", "run", "celery", "-A", "config", "worker", \
     "-l", "info", "-c", "4", "--max-tasks-per-child", "1000"]

FROM base AS beat
CMD ["uv", "run", "celery", "-A", "config", "beat", \
     "-l", "info", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"]
```

**`docker/docker-compose.prod.yml`**

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

## 24. CI/CD Pipeline

### `.github/workflows/ci.yml`

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
      - run: uv sync --group dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy apps/

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: fintrack_test
          POSTGRES_USER: fintrack
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: --health-cmd "redis-cli ping"

    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --group dev
      - run: uv run pytest --cov --cov-report=xml -n auto
        env:
          DATABASE_URL: postgres://fintrack:test@localhost/fintrack_test
          REDIS_URL: redis://localhost:6379/0
          DJANGO_SETTINGS_MODULE: config.settings.testing

      - uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --group dev
      - run: uv run playwright install --with-deps chromium
      - run: uv run pytest tests/e2e/ --browser chromium

  deploy:
    needs: [lint, test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          echo "Deploy steps here (Fly.io / Railway / custom server)"
```

---

## 25. Monitoring & Observability

### Sentry Integration

```python
# config/settings/production.py

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
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
```

### Health Check Endpoint

```
GET /health/
```

Returns JSON with status of: database, cache, storage, celery worker.

### Custom Metrics (Prometheus-compatible)

```python
# apps/core/metrics.py
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from apps.finance.models import Transaction

def metrics_view(request):
    """Simple Prometheus text metrics endpoint."""
    User = get_user_model()
    lines = [
        f"fintrack_users_total {User.objects.count()}",
        f"fintrack_transactions_total {Transaction.all_objects.count()}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
```

---

## 26. ADR Log

### ADR-001: Hypermedia-First Architecture (HTMX over SPA)

| Field | Value |
|---|---|
| **Date** | 2026-04-30 |
| **Status** | Accepted |
| **Decision** | Use HTMX for all dynamic UI; no React/Vue SPA |
| **Rationale** | Simpler stack, Django as single source of truth, no API versioning, better SEO, lower JS payload |
| **Consequences** | Heavy JS client-side logic requires Hyperscript or small vanilla JS; WebSocket features need extra care |

### ADR-002: uv as Package Manager

| Field | Value |
|---|---|
| **Date** | 2026-04-30 |
| **Status** | Accepted |
| **Decision** | Use uv instead of pip/poetry/pipenv |
| **Rationale** | 10-100× faster installs, built-in lockfile, PEP 517/518 compliant, single tool |
| **Consequences** | Team must install uv; CI requires `astral-sh/setup-uv` action |

### ADR-003: DaisyUI v5 + TailwindCSS v4

| Field | Value |
|---|---|
| **Date** | 2026-04-30 |
| **Status** | Accepted |
| **Decision** | Use DaisyUI component classes over custom CSS |
| **Rationale** | Semantic component classes reduce template verbosity; built-in theming; accessibility defaults |
| **Consequences** | Must upgrade when DaisyUI major versions break class names; some design constraints imposed |

### ADR-004: Service Layer Pattern

| Field | Value |
|---|---|
| **Date** | 2026-04-30 |
| **Status** | Accepted |
| **Decision** | All business logic lives in `services/` modules, not views or models |
| **Rationale** | Testability, reusability (CLI commands, Celery tasks, admin), separation of concerns |
| **Consequences** | Slightly more files/indirection; service classes must be instantiated in views |

### ADR-005: UUID Primary Keys

| Field | Value |
|---|---|
| **Date** | 2026-04-30 |
| **Status** | Accepted |
| **Decision** | All domain models use UUID PKs |
| **Rationale** | No sequential ID enumeration in URLs, safe for distributed insert, better for data export |
| **Consequences** | Slightly larger index size; URL patterns use `<uuid:pk>` |

### ADR-006: Soft Delete for Financial Data

| Field | Value |
|---|---|
| **Date** | 2026-04-30 |
| **Status** | Accepted |
| **Decision** | Financial records are soft-deleted (flagged deleted_at), never hard-deleted |
| **Rationale** | Audit trail preservation, balance integrity, regulatory compliance, accidental deletion recovery |
| **Consequences** | Every query on domain models must use the `SoftDeleteManager`; admin needs custom queryset |

---

## 27. Glossary

| Term | Definition |
|---|---|
| **HTMX** | Library enabling HTML elements to make HTTP requests and swap responses into the DOM |
| **Hyperscript** | Scripting language for browser-side behavior using a readable English-like syntax |
| **OOB Swap** | Out-of-Band swap: HTMX feature to update multiple DOM targets from a single response |
| **Hypermedia** | HTML returned by the server as the primary API format (as opposed to JSON) |
| **uv** | Ultra-fast Python package and project manager written in Rust |
| **DaisyUI** | Tailwind plugin providing semantic component class names |
| **Service Layer** | Python classes encapsulating business logic, called by views and tasks |
| **Repository Pattern** | Classes encapsulating database query logic, called by service layer |
| **Soft Delete** | Marking a record as deleted without removing it from the database |
| **Celery Beat** | Celery's periodic task scheduler (cron-like) |
| **ATOMIC_REQUESTS** | Django setting wrapping every view in a DB transaction |
| **HATEOAS** | REST constraint: server responses contain all navigation links for next actions |
| **Base Currency** | User's primary currency for cross-currency balance calculations |
| **RecurringTransaction** | Template for auto-generating periodic transactions (salary, rent, etc.) |

---

*Document version: 1.0.0 — Generated 2026-04-30*
*Maintained by: FinTrack Engineering Team*
