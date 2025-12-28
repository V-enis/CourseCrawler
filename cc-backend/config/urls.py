from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.accounts.views import RegisterView, UserProfileView
urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth endpoints
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Existing Apps
    path("api/", include("apps.courses.urls")),
    path("api/", include("apps.degrees.urls")), 
    path("api/", include("apps.syllabus.urls")),
    path("api/", include("apps.ingestion.urls")),
]