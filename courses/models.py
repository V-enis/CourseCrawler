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
    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

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
    description = models.TextField()
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="beginner",
    )
    url = models.URLField(max_length=250, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ["title"]
        unique_together = ("title", "platform")

    def __str__(self):
        return f"{self.title} ({self.platform})"
    

class CourseVersion(models.Model):
    """
    A Snapshot of a course from a date (Sep 2024, Aug 2026, etc.)
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    syllabus_text = models.JSONField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.course} ({self.created_at})"


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
