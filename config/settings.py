import os
from pathlib import Path

# --- Core Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security Settings ---
# WARNING: The secret key is insecure. A new, strong key MUST be generated for production.
SECRET_KEY = 'django-insecure-simple-key-for-testing-only'

# WARNING: DEBUG should be False in production.
DEBUG = True

# WARNING: Update ALLOWED_HOSTS for production with your actual domain names.
ALLOWED_HOSTS = ['*']

# --- Application Definitions ---
INSTALLED_APPS = [
    'ai_chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',

    # Local apps (The heart of our AI Panel)
    'core',
    'dashboard',
    'users',
    'api_manager',
    'prompt_manager',
]

# --- Middleware Configuration ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- URL Configuration ---
ROOT_URLCONF = 'config.urls'

# --- Template Configuration ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

# --- WSGI Application ---
WSGI_APPLICATION = 'config.wsgi.application'

# --- Database Configuration ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bsepar_panel_db',
        'USER': 'bsepar_panel_user',
        'PASSWORD': 'rwgM1ePwwSdWCQqx2y/uirEL5RtZH0sv',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# --- Static Files Configuration ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# --- Default Primary Key ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Authentication URLs ---
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# --- Authentication Configuration ---
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'users:login'

# --- Authentication Configuration ---
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'users:login'

# --- Authentication Configuration ---
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'users:login'

# --- Authentication Configuration ---
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'users:login'
