from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from .models import College, Program, Student, Organization, Orgmembers

@login_required
def home(request):
    context = {
        'total_organizations': Organization.objects.count(),
        'total_orgmembers': Orgmembers.objects.count(),
        'total_students': Student.objects.count(),
        'total_colleges': College.objects.count(),
        'total_programs': Program.objects.count(),
        # Get top 15 for each category
        'top_organizations': Organization.objects.annotate(
            member_count=Count('orgmembers')).order_by('-member_count')[:15],
        'top_programs': Program.objects.annotate(
            student_count=Count('student')).order_by('-student_count')[:15],
        'recent_students': Student.objects.order_by('-created_at')[:15],
        'recent_colleges': College.objects.order_by('-created_at')[:15],
        'recent_orgmembers': Orgmembers.objects.order_by('-created_at')[:15],
    }
    return render(request, 'home.html', context)

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'
    paginate_by = 10

class ProgramListView(ListView):
    model = Program
    template_name = 'program_list.html'
    context_object_name = 'programs'
    paginate_by = 10

class CollegeListView(ListView):
    model = College
    template_name = 'college_list.html'
    context_object_name = 'colleges'
    paginate_by = 10

class OrganizationListView(ListView):
    model = Organization
    template_name = 'org_list.html'
    context_object_name = 'organizations'
    paginate_by = 10

class OrgmemberListView(ListView):
    model = Orgmembers
    template_name = 'orgmem_list.html'
    context_object_name = 'orgmembers'
    paginate_by = 10

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'student_add.html'
    fields = ['student_id', 'firstname', 'lastname', 'middlename', 'program']
    success_url = reverse_lazy('student-list')

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'student_edit.html'
    fields = ['student_id', 'firstname', 'lastname', 'middlename', 'program']
    success_url = reverse_lazy('student-list')

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')

# Similar views for Program
class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = Program
    template_name = 'program_add.html'
    fields = ['program_name', 'college']
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(LoginRequiredMixin, UpdateView):
    model = Program
    template_name = 'program_edit.html'
    fields = ['program_name', 'college']
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(LoginRequiredMixin, DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')

# Similar views for Organization
class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    template_name = 'org_add.html'
    fields = ['name', 'college', 'description']
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    template_name = 'org_edit.html'
    fields = ['name', 'college', 'description']
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

# Add these College views
class CollegeCreateView(LoginRequiredMixin, CreateView):
    model = College
    template_name = 'college_add.html'
    fields = ['college_name']
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(LoginRequiredMixin, UpdateView):
    model = College
    template_name = 'college_edit.html'
    fields = ['college_name']
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(LoginRequiredMixin, DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')

# Add these Orgmember views
class OrgmemberCreateView(LoginRequiredMixin, CreateView):
    model = Orgmembers
    template_name = 'orgmem_add.html'
    fields = ['student', 'organization', 'date_joined']
    success_url = reverse_lazy('orgmember-list')

class OrgmemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Orgmembers
    template_name = 'orgmem_edit.html'
    fields = ['student', 'organization', 'date_joined']
    success_url = reverse_lazy('orgmember-list')

class OrgmemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Orgmembers
    template_name = 'orgmem_del.html'
    success_url = reverse_lazy('orgmember-list')
