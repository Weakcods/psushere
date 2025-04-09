from django.contrib import admin
from .models import College, Organization, Program, Student, Orgmembers

admin.site.register(College)
admin.site.register(Program)
admin.site.register(Organization)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'firstname', 'lastname', 'middlename', 'program')
    list_filter = ('program',)
    search_fields = ('student_id', 'firstname', 'lastname')

@admin.register(Orgmembers)
class OrgmembersAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization', 'date_joined')
    search_fields = ('student__firstname', 'student__lastname', 'organization__name')