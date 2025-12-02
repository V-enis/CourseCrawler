from rest_framework import serializers

from .models import Semester, Degree
from apps.courses.serializers import CourseSerializer


class SemesterSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Semester
        fields = (
            "id",
            "year",
            "number",
            "theme",
            "courses",
        )


class DegreeSerializer(serializers.ModelSerializer):
    semesters = SemesterSerializer(many=True, read_only=True)

    class Meta:
        model = Degree
        fields = (
            "id",
            "discipline",
            "level",
            "exit_requirements", 
            "semesters"
        )