from rest_framework import generics
from .models import (
    Platform,
    Provider,
    Subject,
    Course,
)
from .serializers import (
    PlatformSerializer,
    ProviderSerializer,
    SubjectSerializer,
    CourseSerializer
)



# Course endpoints
class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Platform, Provider, and Subject endpoints
class PlatformList(generics.ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class ProviderList(generics.ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class SubjectList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
# Create your views here.
