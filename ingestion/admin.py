from django.contrib import admin

from .models import Source, ScrapeJob

admin.site.register(Source)
admin.site.register(ScrapeJob)

# Register your models here.
