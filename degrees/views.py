from rest_framework import generics
from django.shortcuts import get_object_or_404

from .models import Semester, Degree
from .serializers import DegreeSerializer, SemesterSerializer


class DegreeList(generics.ListAPIView):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer



class DegreeDetail(generics.RetrieveAPIView):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer


class DegreeSemesterList(generics.ListAPIView):
    def get_queryset(self):
        degree = get_object_or_404(Degree, pk=self.kwargs['pk'])
        return Semester.objects.filter(degree=degree)
    serializer_class = SemesterSerializer


# Create your views here.
