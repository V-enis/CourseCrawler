from django.core.management.base import BaseCommand, CommandError
from apps.degrees.services import DegreeGenerator
from apps.syllabus.models import CollegeDegree

class Command(BaseCommand):
    help = 'Generates a Degree roadmap from a source CollegeDegree syllabus.'

    def add_arguments(self, parser):
        parser.add_argument('college_degree_id', type=int, help='The ID of the CollegeDegree to use as a source.')

    def handle(self, *args, **options):
        college_degree_id = options['college_degree_id']
        
        # Check if the source syllabus actually exists before starting
        if not CollegeDegree.objects.filter(id=college_degree_id).exists():
            raise CommandError(f"Error: A CollegeDegree with ID '{college_degree_id}' does not exist.")
            
        self.stdout.write(self.style.SUCCESS(f"Starting degree generation for CollegeDegree ID: {college_degree_id}"))
        
        try:
            # Initialize and run the generator service
            generator = DegreeGenerator(college_degree_id)
            generator.generate_roadmap()
            self.stdout.write(self.style.SUCCESS("\nSuccessfully finished generating the degree roadmap."))
        except Exception as e:
            raise CommandError(f"An unexpected error occurred during degree generation: {e}")