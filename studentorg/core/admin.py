from django.contrib import admin
from .models import College, Program, Organization, Student, OrgMember

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'college')
    list_filter = ('college',)
    search_fields = ('name',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'college')
    list_filter = ('college',)
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'lastname', 'firstname', 'program')
    list_filter = ('program',)
    search_fields = ('student_id', 'lastname', 'firstname')

@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization')
    list_filter = ('organization',)
    search_fields = ('student__lastname', 'student__firstname')