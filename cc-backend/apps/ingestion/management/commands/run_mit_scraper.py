import os
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Runs the MIT OCW Scrapy Spider"

    def handle(self, *args, **options):
        # works on Windows AND Docker
        scrapy_project_path = settings.BASE_DIR / "cc_scrapers"

        if not scrapy_project_path.exists():
            self.stdout.write(self.style.ERROR(f"Could not find directory: {scrapy_project_path}"))
            return

        self.stdout.write(self.style.SUCCESS(f"Running spider 'mit' in: {scrapy_project_path}"))

        try:
            subprocess.run(['scrapy', 'crawl', 'mit'], cwd=str(scrapy_project_path), check=True)
            self.stdout.write(self.style.SUCCESS("Spider finished running successfully."))
        except subprocess.CalledProcessError as e:
            self