from django.core.management.base import BaseCommand
from apps.courses.models import Course
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Backfills embeddings for all courses that do not have one.'

    def handle(self, *args, **options):
        # find courses where embeddings is null
        from apps.courses.tasks import generate_embedding_for_course

        courses_to_process = Course.objects.filter(embedding__isnull=True)
        count = courses_to_process.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('All courses already have embeddings. Nothing to do.'))
            return 
        
        self.stdout.write(f"Found {count} courses to backfill. Dispatching tasks...")

        for course in tqdm(courses_to_process.iterator()):
            generate_embedding_for_course.delay(course.id)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully dispatched all {count} backfill tasks to the queue.'))
        self.stdout.write('Check the Celery worker logs to monitor the progress.')