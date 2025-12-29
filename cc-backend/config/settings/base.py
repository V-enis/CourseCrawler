from pathlib import Path
from environs import Env
import os
from datetime import timedelta

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- CORE DJANGO SETTINGS ---
SECRET_KEY = env.str("SECRET_KEY")
ALLOWED_HOSTS = [] # This will be overridden in production.py and local.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd Party
    "corsheaders",
    'rest_framework',
    'django_redis',
    # Local
    'apps.accounts',
    'apps.courses',
    'apps.degrees',
    'apps.syllabus',
    'apps.ingestion',
    'apps.ml',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
TEMPLATES = [ 
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- DATABASE ---
DATABASES = { "default": env.dj_db_url("DATABASE_URL") }

# --- PASSWORD VALIDATION, I18N, ETC. ---
AUTH_PASSWORD_VALIDATORS = [ 
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "accounts.CustomUser"

# --- STATIC FILES ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- DJANGO REST FRAMEWORK ---
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'apps.accounts.utils.PermissiveJWTAuthentication', 
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# --- JWT TOKENS ---
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# --- HUGGING FACE / LOCAL LLM SETTINGS ---
HF_INFERENCE_ENDPOINT_URL = env.str("HF_INFERENCE_ENDPOINT_URL", default="https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct")
# Note: Changing this to HF_TOKEN to be shorter/standard
HF_TOKEN = env.str("HF_TOKEN", default=None)