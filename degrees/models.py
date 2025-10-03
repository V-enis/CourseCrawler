from django.db import models
from courses.models import Course


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
    theme = models.CharField(max_length=200, blank=True)
    courses = models.ManyToManyField(Course, related_name="semesters")

    class Meta:
        ordering = ['year']
        unique_together = ('degree', 'year')

    def __str__(self):
        return f"{self.degree.get_level_display()} Year {self.year}"
    

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
    exit_requirements = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_level_display()} in {self.discipline}"


# Create your models here.
