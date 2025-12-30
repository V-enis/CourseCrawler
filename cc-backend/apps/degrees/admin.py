from django.contrib import admin
from .models import Degree, Semester, Enrollment 

@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ('discipline', 'level', 'degree_id')
    search_fields = ('discipline',)

from django.contrib import admin
from .models import Degree, Semester

class SemesterInline(admin.TabularInline):
    model = Semester
    raw_id_fields = ['courses'] 
    extra = 0

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['degree', 'year', 'number', 'theme']
    raw_id_fields = ['courses']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'enrolled_at')
    list_filter = ('degree',)
    readonly_fields = ('user', 'degree')