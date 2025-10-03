from rest_framework import serializers

from .models import Semester, Degree
from courses.serializers import CourseSerializer


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = (
            "degree_id",
            "discipline",
            "level",
        )


class SemesterSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    degree = DegreeSerializer(read_only=True)

    class Meta:
        model = Semester
        fields = (
            "degree",
            "year",
            "theme",
            "courses",
        )