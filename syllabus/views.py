from rest_framework import generics

from .models import (
    College,
    CollegeDegree,
    Year,
    CollegeSemester,
    CollegeCourse,
)
from .serializers import (
    CollegeSerializer,
    CollegeDegreeSerializer,
    YearSerializer,
    CollegeSemesterSerializer,
    CollegeCourseSerializer,
)

# College
class CollegeList(generics.ListAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

class CollegeDetail(generics.RetrieveAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer


# CollegeDegree
class CollegeDegreeList(generics.ListAPIView):
    queryset = CollegeDegree.objects.all()
    serializer_class = CollegeDegreeSerializer

class CollegeDegreeDetail(generics.RetrieveAPIView):
    queryset = CollegeDegree.objects.all()
    serializer_class = CollegeDegreeSerializer


# Year
class YearList(generics.ListAPIView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer

class YearDetail(generics.RetrieveAPIView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer


# College Semester
class CollegeSemesterList(generics.ListAPIView):
    queryset = CollegeSemester.objects.all()
    serializer_class = CollegeSemesterSerializer

class CollegeSemesterDetail(generics.RetrieveAPIView):
    queryset = CollegeSemester.objects.all()
    serializer_class = CollegeSemesterSerializer


# College Course
class CollegeCourseList(generics.ListAPIView):
    queryset = CollegeCourse.objects.all()
    serializer_class = CollegeCourseSerializer

class CollegeCourseDetail(generics.RetrieveAPIView):
    queryset = CollegeCourse.objects.all()
    serializer_class = CollegeCourseSerializer




# Create your views here.
