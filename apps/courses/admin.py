from django.contrib import admin

from .models import Platform, Provider, Subject, Course, CourseVersion, Resource

admin.site.register(Platform)
admin.site.register(Provider)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(CourseVersion)
admin.site.register(Resource)

# Register your models here.
