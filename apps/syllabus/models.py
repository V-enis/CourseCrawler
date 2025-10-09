from django.db import models

from apps.courses.models import Subject


class College(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class CollegeDegree(models.Model):
    LEVEL_CHOICES = [
        ("ASSOC", "Associate"),
        ("BACH", "Bachelor"),
        ("MAST", "Master"),
    ]

    degree_id = models.CharField(max_length=20, unique=True)   
    title = models.CharField(max_length=200)       
    college = models.ForeignKey(
        "College",
        on_delete=models.PROTECT,
        related_name="degrees",
        null=True,
        blank=True,
        )            
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    overview = models.TextField(blank=True)                   
    learning_outcomes = models.TextField(blank=True)          
    exit_requirements = models.TextField(blank=True)        

    class Meta:
        ordering = ["title"]
        unique_together = ("college", "title")

    def __str__(self):
        return f"{self.get_level_display()} in {self.title}"


class Year(models.Model):
    """
    Optional grouping to cluster semesters (1st year, 2nd year, etc.).
    """
    degree = models.ForeignKey(CollegeDegree, on_delete=models.PROTECT, related_name="years")
    number = models.PositiveSmallIntegerField()              
    description = models.TextField(blank=True)                 

    class Meta:
        ordering = ["degree", "number"]
        unique_together = ("degree", "number")

    def __str__(self):
        return f"{self.degree.title} - Year {self.number}"


class CollegeCourse(models.Model):
    CATEGORY_CHOICES = [
        ("GENED", "General Education"),
        ("FOUND", "Foundation"),
        ("CORE", "Core Major"),
        ("ELECT", "Elective"),
        ("CAP", "Capstone"),
        ("RES", "Research"),
    ]
    title = models.CharField(max_length=100)
    course_id = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True
    )
    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="required_for",
        )
    completion_criteria = models.TextField(blank=True)
    semester = models.ForeignKey(
        "CollegeSemester",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )

    def __str__(self):
        return f"{self.title} - {self.course_id}" 
    

class CollegeSemester(models.Model):
    year = models.ForeignKey(Year, on_delete=models.PROTECT, related_name="semesters")
    theme = models.CharField(max_length=200, blank=True)
    courses = models.ManyToManyField(CollegeCourse, related_name="semesters")
    number = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["year", "number"]
        unique_together = ("year", "number")

    def __str__(self):
        return f"{self.year.degree.title} - Year {self.year.number} Sem {self.number}"





# Create your models here.
