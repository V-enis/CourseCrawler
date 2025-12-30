from .base import * # Inherit all settings from base.py
import ssl 

# --- PRODUCTION-SPECIFIC SETTINGS ---

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"]) 

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# --- DATABASE ---
DATABASES = {
    "default": env.dj_db_url("DATABASE_URL")
}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60) 


# --- CACHE ---
# We use database '1' on our Redis instance for caching
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # Use the raw URL from env (don't add /1 manually here, let django-redis handle it via OPTIONS if needed, 
        # or rely on the default db 0 if /1 causes issues. Standard practice is to just use the URL).
        "LOCATION": env.str("REDIS_URL"), 
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # This handles the SSL certificate issue cleanly
            "CONNECTION_POOL_KWARGS": {
                "ssl_cert_reqs": ssl.CERT_NONE
            }
        }
    }
}


# --- CELERY ---
# Celery will use database '0' on our Redis instance
from celery.schedules import crontab

CELERY_BROKER_URL = env.str("REDIS_URL") 
CELERY_RESULT_BACKEND = env.str("REDIS_URL")

CELERY_REDIS_BACKEND_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE}
CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE}

CELERY_BEAT_SCHEDULE = {
    'run-mit-scraper-weekly': {
        'task': 'apps.ingestion.tasks.run_mit_ocw_scraper',
        'schedule': crontab(minute='5', hour='4', day_of_week='sun'),
    },
}


# --- CORS (CROSS-ORIGIN RESOURCE SHARING) ---
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])


# --- SECURITY MIDDLEWARE SETTINGS ---
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=60) # Start with a small value
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)