from django.db import models


class Source(models.Model):
    SOURCE_TYPES = [
        ("WEBSITE", "Website"),
        ("API", "API"),
        ("PDF", "PDF")
    ]
    
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(blank=True)
    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES,
        default="WEBSITE"
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class ScrapeJob(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed")
    ]

    source = models.ForeignKey(
        Source, 
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    output_file = models.FileField(upload_to="scrapes/", blank=True, null=True)
    error_log = models.TextField(blank=True)

    def __str__(self):
        return f"{self.source.name} scrape at {self.started_at} [{self.status}]"

# Create your models here.
