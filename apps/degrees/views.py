from rest_framework import viewsets, permissions
from .models import Degree
from .serializers import DegreeSerializer 

class DegreeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Degrees: both a 'list' of all degrees and a 'retrieve' action for a single
    degree's full nested details (semesters and courses).
    """
    queryset = Degree.objects.all().prefetch_related(
        'semesters__courses__platform',
        'semesters__courses__provider'
    )
    permission_classes = [permissions.AllowAny] # Allow public read-only access.
    serializer_class = DegreeSerializer 