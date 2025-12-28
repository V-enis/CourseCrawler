from django.contrib import admin
from .models import Degree, Semester, Enrollment 

@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ('discipline', 'level', 'degree_id')
    search_fields = ('discipline',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'degree', 'year', 'number')
    list_filter = ('year', 'degree')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'enrolled_at')
    list_filter = ('degree',)
    readonly_fields = ('user', 'degree')