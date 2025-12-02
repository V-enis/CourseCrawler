from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from .tasks import generate_embedding_for_course

@receiver(post_save, sender=Course)
def trigger_embedding_generation(sender, instance, created, update_fields, **kwargs):
    """
    When a course is saved, trigger the Celery task to create its embedding. 
    Add check to avoid an infinite loop if only the embedding is saved. 
    """
    if update_fields is None or list(update_fields) != ['embedding']:
        print(f"Signal recieved for course {instance.id}. Dispatching embedding task.")
        generate_embedding_for_course.delay(instance.id)