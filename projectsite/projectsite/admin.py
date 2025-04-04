from django.contrib import admin
from .models import College,Organization, Program, Student, Orgmembers

admin.site.register(College)
admin.site.register(Program)
admin.site.register(Organization)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'middle_name', 'program')
    list_filter = ('program',)
    search_fields = ('student_id', 'first_name', 'last_name')

@admin.register(Orgmembers)
class OrgmembersAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization', 'date_joined')
    search_fields = ('student__first_name', 'student__last_name', 'organization__name')

    def get_member_name(self, obj):
        try:
            member = Student.objects.get(id=obj.student_id)
            return member.program
        except Student.DoesNotExist:
            return None