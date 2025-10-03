from rest_framework import serializers

from .models import (
    Platform,
    Provider,
    Subject,
    Course,
    CourseVersion,
    Resource
)


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields =(
            "id",
            "name",
            "website",
            "description",
        )


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            "id",
            "name",
            "website",
            "description",
        )


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name",)    


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "platform",
            "subjects",
            "description",
            "category",
            "is_active",
            "url",
        )
    

class CourseVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseVersion
        fields = (
            "id",
            "course",
            "syllabus_text",
            "created_at",
        )

    
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = (
            "id",
            "title",
            "resource_type",
            "url",
            "platform",
        )