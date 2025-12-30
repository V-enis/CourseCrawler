from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Degree, Enrollment
from .serializers import DegreeSerializer, EnrollmentSerializer

class DegreeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Degrees.
    
    - The main `list` view is cached for 15 minutes for high performance.
    - The user-specific `my_enrollments` view is never cached to ensure data is always fresh.
    """
    queryset = Degree.objects.all().prefetch_related(
        'semesters__courses__platform',
        'semesters__courses__provider',
        'semesters__courses__subjects',
    )
    permission_classes = [permissions.AllowAny]
    serializer_class = DegreeSerializer 
    lookup_field = 'slug'

    @method_decorator(cache_page(60 * 15)) # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



    # This is a POST request, so it is not affected by caching.
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, slug=None):
        degree = self.get_object()
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, degree=degree)
        if created:
            # Return 201 Created for a new enrollment
            return Response({'status': 'enrolled'}, status=status.HTTP_201_CREATED)
        # Return 200 OK if they were already enrolled
        return Response({'status': 'already enrolled'}, status=status.HTTP_200_OK)
    
    # This GET request is intentionally NOT cached to ensure it's always up-to-date.
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_enrollments(self, request):
        enrollments = Enrollment.objects.filter(user=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True, context={'request': request})
        return Response(serializer.data)