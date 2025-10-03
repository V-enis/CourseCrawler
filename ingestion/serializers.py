from rest_framework import serializers
from .models import Source, ScrapeJob


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "name", "base_url", "source_type", "description"]


class ScrapeJobSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source="source.name", read_only=True)
    
    class Meta: 
        model = ScrapeJob
        fields = [
            "id",
            "source",
            "source_name",
            "status",
            "started_at",
            "finished_at",
            "output_file",
            "error_log",
        ]
        read_only_fields = ["status", "started_at", "finished_at", "output_file", "error_log"]