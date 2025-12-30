from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from .tasks import generate_embedding_for_course

@receiver(post_save, sender=Course)
def trigger_embedding_generation(sender, instance, created, **kwargs):
    """
    When a Course is saved, trigger the Celery task to generate its embedding,
    but ONLY if one is actually needed. This prevents redundant task queuing.
    """
    from .tasks import generate_embedding_for_course

    update_fields = kwargs.get('update_fields') or frozenset()

    # The fields that, if changed, require a new embedding.
    embedding_source_fields = {'title', 'description', 'subjects', 'learning_outcomes', 'category', 'prerequisites'}

    # Check if any of the changed fields are ones that contribute to the embedding.
    source_fields_changed = bool(embedding_source_fields.intersection(update_fields))

    # We dispatch a task under three conditions:
    # 1. The course is brand new.
    # 2. The course is being updated, a source field changed, and we want to regenerate the embedding.
    # 3. The course is being saved for any other reason, but is missing an embedding.
    if created or source_fields_changed or not instance.embedding:
        # One final check to prevent a loop if the embedding task itself uses .save()
        if 'embedding' in update_fields and len(update_fields) == 1:
            return

        print(f"Signal: Course {instance.id} needs an embedding. Dispatching task.")
        generate_embedding_for_course.delay(instance.id)