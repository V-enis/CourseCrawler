from celery import shared_task
from sentence_transformers import SentenceTransformer
from .models import Course
import numpy as np

# Load model once when the worker starts
print("Loading sentence transformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded successfully.")

@shared_task
def generate_embedding_for_course(course_id):
    """
    A Celery task to generate and save an embedding for a single course.
    """
    try:
        course = Course.objects.get(id=course_id)
        text_to_embed = course.get_text_for_embedding()

        if not text_to_embed:
            print(f"Course {course_id} has no text to embed. Skipping embedding.")
            return f"Skipped course {course_id}. No text content"
        
        print(f"Generating embedding for Course ID:{course_id}...")
        embedding = model.encode(text_to_embed)

        Course.objects.filter(id=course_id).update(embedding=embedding.tolist())

        print(f"Successfully saved embedding for Course ID: {course_id}")
        return f"Successfully generated embedding for course {course_id}"
    
    except Course.DoesNotExist:
        print(f"Course with id {course_id} not found for embedding generation.")
        return f"Error: course with id {course_id} not found."
    except Exception as e:
        print(f"An unexpected error occurred with course {course_id}: {e}")
        return f"Error: {e}"