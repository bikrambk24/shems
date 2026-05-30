from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────────────────────
# SECURITY — core secrets and debug flag
# ──────────────────────────────────────────────────────────────

# In production, move this to an environment variable instead of hardcoding it.
SECRET_KEY = 'django-insecure-shems-dev-key-change-before-production'

# Never run with DEBUG=True on a public server — it exposes stack traces.
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']  # 'testserver' needed for Django test client

# ──────────────────────────────────────────────────────────────
# APPS
# ──────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # SHEMS apps — accounts must come first because it defines AUTH_USER_MODEL
    'accounts.apps.AccountsConfig',
    'appliances.apps.AppliancesConfig',
    'energy.apps.EnergyConfig',
    'pricing.apps.PricingConfig',
    'core.apps.CoreConfig',
]

# ──────────────────────────────────────────────────────────────
# MIDDLEWARE
# ──────────────────────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',            # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking
]

ROOT_URLCONF = 'shems.urls'

# ──────────────────────────────────────────────────────────────
# TEMPLATES
# ──────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Look in the top-level templates/ folder first
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shems.wsgi.application'

# ──────────────────────────────────────────────────────────────
# DATABASE — SQLite, no extra setup required
# ──────────────────────────────────────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ──────────────────────────────────────────────────────────────
# AUTHENTICATION — custom User model (MUST be set before first migration)
# ──────────────────────────────────────────────────────────────

# Tells Django to use our custom User model instead of the built-in one.
# This cannot be changed after the first migration without resetting the database.
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ──────────────────────────────────────────────────────────────
# LOGIN / LOGOUT ROUTING
# ──────────────────────────────────────────────────────────────

LOGIN_URL = '/login/'

# After login, send users to a view that reads their role and redirects them
# to the correct dashboard (homeowner / admin / technician).
LOGIN_REDIRECT_URL = '/role-redirect/'

LOGOUT_REDIRECT_URL = '/login/'

# ──────────────────────────────────────────────────────────────
# INTERNATIONALISATION
# ──────────────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────────
# STATIC FILES
# ──────────────────────────────────────────────────────────────

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ──────────────────────────────────────────────────────────────
# SECURITY HEADERS (safe to enable in development too)
# ──────────────────────────────────────────────────────────────

X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
