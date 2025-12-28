from .base import * # Inherit all settings from base.py

# --- LOCAL DEVELOPMENT-SPECIFIC SETTINGS ---

DEBUG = True

# local development
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "127.0.0.1:3000"]

# CORS settings for local development (allow React dev server)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'run-mit-scraper-hourly': {
        'task': 'apps.ingestion.tasks.run_mit_ocw_scraper',
        'schedule': crontab(minute=0, hour='*'), # Every hour
    },
}