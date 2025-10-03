from django.urls import path

from .views import (
    CollegeList,
    CollegeDetail,
    CollegeDegreeList,
    CollegeDegreeDetail,
    YearList,
    YearDetail,
    CollegeSemesterList,
    CollegeSemesterDetail,
    CollegeCourseList,
    CollegeCourseDetail
)

urlpatterns = [
    path("", CollegeDegreeList.as_view(), name="degree_list"),
    path("<int:pk>/", CollegeDegreeDetail.as_view(), name="degree_detail"),
    path("<int:pk>/semester/<int:semester_pk>/", CollegeSemesterDetail.as_view(), name="semester_detail"),
    path("<int:pk>/course/<int:course_pk>/", CollegeCourseDetail.as_view(), name="course_detail"),
]
