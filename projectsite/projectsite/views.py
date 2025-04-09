from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import College, Program, Student, Organization, Orgmembers

@login_required
def home(request):
    return render(request, 'home.html')

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
