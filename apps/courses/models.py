from django.db import models


class Platform(models.Model):
    """
    Represents an online learning platform (edX, Coursera, Udemy, etc.)
    """
    name = models.CharField(max_length=150, unique=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Provider(models.Model):
    """
    Organization or university offering the course (MITx, Google, Stanford Online)
    """
    name = models.CharField(max_length=150, unique=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Subject(models.Model):
    """
    High-level categorization (Computer Science, Mathematics, AI, etc.).
    Used to filter/search courses.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    A single online course 
    """
    CATEGORY_CHOICES = [
        ("GENED", "General Education"),
        ("FOUND", "Foundation"),
        ("CORE", "Core Major"),
        ("ELECT", "Elective"),
        ("CAP", "Capstone"),
        ("RES", "Research"),
    ]

    code = models.CharField(max_length=20, unique=True, null=True, blank=True) 
    title = models.CharField(max_length=100)
    slug = models.SlugField(default="", null=False)
    platform = models.ForeignKey(
        Platform,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="courses"
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="courses",
    )
    subjects = models.ManyToManyField(Subject, related_name="courses")
    description = models.TextField(blank=True)
    learning_outcomes = models.TextField(blank=True)
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        blank=True,
    )

    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="unlocks"
    )
    url = models.URLField(max_length=250, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(blank=True, null=True)

    active_version = models.ForeignKey(
        "CourseVersion",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="current_for"
    )
    
    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.platform or 'N/A'})"
    

class CourseVersion(models.Model):
    """
    A Snapshot of a course from a date (Sep 2024, Aug 2026, etc.)
    """
   
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    version = models.CharField(max_length=50, default="v1")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    syllabus_json = models.JSONField(blank=True, null=True)
    learning_outcomes = models.TextField(blank=True)
    assessment_type = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course} ({self.version})"


class Resource(models.Model):
    """
    A learning object (video, article, book, paper) linked
    either directly to a CourseVersion or used in a roadmap.
    """
    RESOURCE_TYPE = [
        ("video", "Video"),
        ("article", "Article"),
        ("book", "Book"),
        ("paper", "Paper"),
        ("repo", "Repository")
    ]
    
    title = models.CharField(max_length=150)
    resource_type = models.CharField(
        max_length=7,
        choices=RESOURCE_TYPE,
        null=True,
        blank=True,
    )
    url = models.URLField(max_length=250, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(blank=True, null=True)
    platform = models.ForeignKey(
        Platform,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="resources"
    )


# Create your models here.
