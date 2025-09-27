from django.urls import path

from .views import (
    CourseList,
    CourseDetail,
    PlatformList,
    ProviderList,
    SubjectList,
)

urlpatterns = [
    path("", CourseList.as_view(), name="course_list"),
    path("<int:pk>/", CourseDetail.as_view(), name="course_detail"),
    path("platforms/", PlatformList.as_view(), name="platform_list"),
    path("providers/", ProviderList.as_view(), name="provider_list"),
    path("subjects/", SubjectList.as_view(), name="subject_list"),
]
