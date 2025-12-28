from django.contrib import admin
from .models import Course, Platform, Provider, Subject 

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'display_subjects', 'is_active') 
    list_filter = ('platform', 'provider', 'is_active')
    search_fields = ('title', 'description', 'code') 
    
    def display_subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subjects.all()])
    display_subjects.short_description = 'Subjects' # Sets the column header

admin.site.register(Platform)
admin.site.register(Provider)
admin.site.register(Subject)