from django.core.management.base import BaseCommand
from apps.ingestion.tasks import run_mit_ocw_scraper

class Command(BaseCommand):
    help = 'Sends a test task to the Celery worker.'

    def handle(self, *args, **options):
        self.stdout.write("Attempting to send task to Celery...")
        try:
            run_mit_ocw_scraper.delay()
            self.stdout.write(self.style.SUCCESS("Successfully sent the task to the queue!"))
            self.stdout.write("Check the worker logs to see if it gets picked up.")
        except Exception as e:
            self.stdout.write(self.style.ERROR("Failed to send the task."))
            self.stdout.write(self.style.ERROR(f"Error: {e}"))