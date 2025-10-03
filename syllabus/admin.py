from django.contrib import admin

from .models import (
    College,
    CollegeDegree,
    Year,
    CollegeSemester,
    CollegeCourse
)

admin.site.register(College)
admin.site.register(CollegeDegree)
admin.site.register(Year)
admin.site.register(CollegeSemester)
admin.site.register(CollegeCourse)

# Register your models here.
