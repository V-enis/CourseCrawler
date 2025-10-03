from rest_framework import serializers
from .models import (
    College, 
    CollegeDegree, 
    Year,
    CollegeCourse, 
    CollegeSemester,
)

class CollegeCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeCourse
        fields = (
            "title",
            "course_id",
            "description",
            "category",
            "prerequisites",
            "completion_criteria",
        )

class CollegeSemesterSerializer(serializers.ModelSerializer):
    courses = CollegeCourseSerializer(many=True, read_only=True)

    class Meta:
        model = CollegeSemester
        fields = (
            "year",
            "theme",
            "courses",
            "number",
        )


class YearSerializer(serializers.ModelSerializer):
    semesters = CollegeSemesterSerializer(many=True, read_only=True)
    class Meta:
        model = Year
        fields = (
            "degree",
            "number",
            "description",
            "semesters",
        )


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = (
            "title",
            "description",
        )



class CollegeDegreeSerializer(serializers.ModelSerializer):
    years = YearSerializer(many=True, read_only=True)
    college = CollegeSerializer(read_only=True)

    class Meta:
        model = CollegeDegree
        fields = (
            "degree_id",
            "title",
            "college",
            "level",
            "overview",
            "years",
            "learning_outcomes",
            "exit_requirements",
        )