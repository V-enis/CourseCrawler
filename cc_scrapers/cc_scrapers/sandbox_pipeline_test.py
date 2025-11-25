import sys
import os
import django

# Add Django project root to sys.path
sys.path.append(r'C:\Users\lilit\Desktop\Dev\personal-projects\CourseCrawler\cc-backend')

# Point to Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
django.setup()


from pipelines import SaveToDjangoPipeline

pipeline = SaveToDjangoPipeline()

fake_item = {
    'url': 'https://ocw.mit.edu/courses/6-001-introduction-to-computer-science/',
    'title': 'Intro to Computer Science',
    'description': 'An introduction to computer science and programming concepts.',
    'subjects': ['Computer Science', 'Programming'],
    'platform': 'MIT OCW',
    'provider': 'MITx',
}

pipeline.process_item(fake_item, spider=None)