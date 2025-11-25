import os
from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = "Runs the MIT OCW Scrapy Spider"

    def handle(self, *args, **options):
        scrapy_project_path = "/code/cc_scrapers"
        spider_name = "mit"

        self.stdout.write(self.style.SUCCESS(f"Changing directory to {scrapy_project_path}"))
        os.chdir(scrapy_project_path)
        self.stdout.write(self.style.SUCCESS(f"Running spider: {spider_name}"))

        subprocess.run(['scrapy', 'crawl', spider_name])

        self.stdout.write(self.style.SUCCESS("Spider finished running."))
        