from django.urls import path

from .views import (
    DegreeList,
    DegreeDetail,
    DegreeSemesterList,
)

urlpatterns = [
    path("", DegreeList.as_view(), name="degree_list"),
    path("<int:pk>/", DegreeDetail.as_view(), name="degree_detail"),
    path("<int:pk>/semesters/", DegreeSemesterList.as_view(), name="degree_semester_list"),
]
