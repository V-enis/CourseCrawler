from rest_framework import serializers

from .models import Semester, Degree, Enrollment
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
            "degree_id",
            "slug",
            "discipline",
            "level",
            'description',
            "exit_requirements", 
            "semesters"
        )


class EnrollmentSerializer(serializers.ModelSerializer):
    degree = DegreeSerializer(read_only=True)

    class Meta: 
        model = Enrollment
        fields = ['id', 'degree', 'enrolled_at']