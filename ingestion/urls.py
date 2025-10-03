from django.urls import path
from .views import SourceList, ScrapeJobList, ScrapeJobDetail, ScrapeJobCreate

urlpatterns = [
    path("sources/", SourceList.as_view(), name="source_list"),
    path("jobs/", ScrapeJobList.as_view(), name="job_list"),
    path("jobs/<int:pk>/", ScrapeJobDetail.as_view(), name="job_detail"),
    path("jobs/create/", ScrapeJobCreate.as_view(), name="job_create"),
]
