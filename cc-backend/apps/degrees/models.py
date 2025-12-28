from django.db import models
from django.conf import settings
from apps.courses.models import Course
from django.utils.text import slugify


class Semester(models.Model):
    """
    One semester in a degree
    """
    degree = models.ForeignKey(
        'Degree',
        on_delete=models.PROTECT,
        related_name='semesters',
    )
    year = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField(default=1)
    theme = models.CharField(max_length=200, blank=True)
    courses = models.ManyToManyField(Course, related_name="semesters")

    class Meta:
        ordering = ['year', 'number']
        unique_together = ('degree', 'year', 'number')

    def __str__(self):
        return f"{self.degree} - Year {self.year}, Sem {self.number}"
    

class Degree(models.Model):
    """
    Models for degrees, programs, and semesters.
    Organizes courses into structured, roadmap-like academic tracks.
    """
    DEGREE_LEVEL_CHOICES = [
        ("ASSOC", "Associate"),
        ("BACH", "Bachelor"),
        ("MAST", "Master"),
    ]

    degree_id = models.CharField(max_length=20, unique=True)
    discipline = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=DEGREE_LEVEL_CHOICES)
    description = models.TextField(blank=True)
    exit_requirements = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate the slug from the discipline and level if it doesn't exist
        if not self.slug:
            base_slug = slugify(f"{self.get_level_display()} in {self.discipline}")
            self.slug = base_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_level_display()} in {self.discipline}"


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    degree = models.ForeignKey('Degree', on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'degree')

    def __str__(self):
        return f"{self.user} -> {self.degree}"
# Create your models here.
