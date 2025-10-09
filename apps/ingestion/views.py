from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Source, ScrapeJob
from .serializers import SourceSerializer, ScrapeJobSerializer

class SourceList(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class ScrapeJobList(generics.ListAPIView):
    serializer_class = ScrapeJobSerializer

    def get_queryset(self):
        source_id = self.request.query_params.get("source")
        if source_id:
            return ScrapeJob.objects.filter(source_id=source_id).order_by("-started_at")
        return ScrapeJob.objects.all().order_by("-started_at")


class ScrapeJobDetail(generics.RetrieveAPIView):
    queryset = ScrapeJob.objects.all()
    serializer_class = ScrapeJobSerializer
    

class ScrapeJobCreate(generics.CreateAPIView):
    serializer_class = ScrapeJobSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        source = get_object_or_404(Source, pk=request.data.get("source"))

        job = ScrapeJob.objects.create(source=source, status="PENDING")

        serializer = self.get_serializer(job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Create your views here.
