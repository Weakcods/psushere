from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.template import RequestContext
from .models import College, Program, Student, Organization, Orgmembers
from collections import defaultdict
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection

def logout_view(request):
    logout(request)
    return redirect('login')

def handler404(request, exception):
    context = {}
    response = render(request, "404.html", context)
    response.status_code = 404
    return response

@login_required
def home(request):
    with connection.cursor() as cursor:
        # Get totals in a single query
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM projectsite_organization) as total_organizations,
                (SELECT COUNT(*) FROM projectsite_student) as total_students,
                (SELECT COUNT(*) FROM projectsite_program) as total_programs,
                (SELECT COUNT(*) FROM projectsite_college) as total_colleges
        """)
        totals = cursor.fetchone()
        total_organizations, total_students, total_programs, total_colleges = totals

        # Get program statistics efficiently
        cursor.execute("""
            SELECT 
                p.program_name,
                COUNT(s.id) as student_count
            FROM projectsite_program p
            LEFT JOIN projectsite_student s ON s.program_id = p.id
            GROUP BY p.id, p.program_name
            ORDER BY student_count DESC
            LIMIT 5
        """)
        program_stats = [
            {'program_name': row[0], 'student_count': row[1]}
            for row in cursor.fetchall()
        ]

        # Get organization growth by month efficiently
        cursor.execute("""
            SELECT 
                strftime('%Y', date_joined) as year,
                strftime('%m', date_joined) as month,
                COUNT(*) as member_count
            FROM projectsite_orgmembers
            GROUP BY year, month
            ORDER BY year, month
        """)
        org_growth = [
            {'year': int(row[0]), 'month': int(row[1]), 'member_count': row[2]}
            for row in cursor.fetchall()
        ]

        # Get college distribution with a single query
        cursor.execute("""
            SELECT 
                c.college_name,
                COUNT(DISTINCT s.id) as student_count,
                COUNT(DISTINCT o.id) as org_count
            FROM projectsite_college c
            LEFT JOIN projectsite_program p ON p.college_id = c.id
            LEFT JOIN projectsite_student s ON s.program_id = p.id
            LEFT JOIN projectsite_organization o ON o.college_id = c.id
            GROUP BY c.id, c.college_name
        """)
        college_distribution = [
            {
                'college_name': row[0],
                'student_count': row[1],
                'org_count': row[2]
            }
            for row in cursor.fetchall()
        ]

        # Get student registrations by month
        cursor.execute("""
            SELECT 
                strftime('%Y', created_at) as year,
                strftime('%m', created_at) as month,
                COUNT(*) as count
            FROM projectsite_student
            GROUP BY year, month
            ORDER BY year, month
        """)
        student_registrations = [
            {'year': int(row[0]), 'month': int(row[1]), 'count': row[2]}
            for row in cursor.fetchall()
        ]

        # Get organization member distribution
        cursor.execute("""
            SELECT 
                o.name,
                COUNT(om.id) as member_count
            FROM projectsite_organization o
            LEFT JOIN projectsite_orgmembers om ON om.organization_id = o.id
            GROUP BY o.id, o.name
            ORDER BY member_count DESC
            LIMIT 8
        """)
        org_member_dist = [
            {'name': row[0], 'member_count': row[1]}
            for row in cursor.fetchall()
        ]

    context = {
        'total_organizations': total_organizations,
        'total_students': total_students,
        'total_programs': total_programs,
        'total_colleges': total_colleges,
        'program_stats': program_stats,
        'org_growth': org_growth,
        'college_distribution': college_distribution,
        'student_registrations': student_registrations,
        'org_member_dist': org_member_dist,
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    # Use raw SQL for complex aggregations
    with connection.cursor() as cursor:
        # Get totals in a single query
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM projectsite_student) as total_students,
                (SELECT COUNT(*) FROM projectsite_organization) as total_orgs,
                (SELECT COUNT(*) FROM projectsite_orgmembers) as total_members,
                (SELECT COUNT(*) FROM projectsite_program) as total_programs
        """)
        totals = cursor.fetchone()
        total_students, total_orgs, total_members, total_programs = totals

        # Get monthly registrations using efficient date extraction
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', created_at) as month,
                COUNT(*) as count
            FROM projectsite_student
            GROUP BY strftime('%Y-%m', created_at)
            ORDER BY month
        """)
        formatted_registrations = [
            {'month': row[0], 'count': row[1]}
            for row in cursor.fetchall()
        ]

        # College-wise student distribution with a single JOIN
        cursor.execute("""
            SELECT 
                c.college_name,
                COUNT(DISTINCT s.id) as student_count
            FROM projectsite_college c
            LEFT JOIN projectsite_program p ON p.college_id = c.id
            LEFT JOIN projectsite_student s ON s.program_id = p.id
            GROUP BY c.id, c.college_name
        """)
        college_stats = [
            {'college_name': row[0], 'student_count': row[1]}
            for row in cursor.fetchall()
        ]

        # Program popularity with efficient counting
        cursor.execute("""
            SELECT 
                p.program_name,
                COUNT(s.id) as student_count
            FROM projectsite_program p
            LEFT JOIN projectsite_student s ON s.program_id = p.id
            GROUP BY p.id, p.program_name
            ORDER BY student_count DESC
            LIMIT 5
        """)
        program_stats = [
            {'program_name': row[0], 'student_count': row[1]}
            for row in cursor.fetchall()
        ]

        # Organization membership trends
        cursor.execute("""
            SELECT 
                o.name,
                COUNT(om.id) as member_count
            FROM projectsite_organization o
            LEFT JOIN projectsite_orgmembers om ON om.organization_id = o.id
            GROUP BY o.id, o.name
            ORDER BY member_count DESC
            LIMIT 5
        """)
        org_trends = [
            {'name': row[0], 'member_count': row[1]}
            for row in cursor.fetchall()
        ]

        # Monthly organization growth
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', date_joined) as month,
                COUNT(*) as count
            FROM projectsite_orgmembers
            GROUP BY strftime('%Y-%m', date_joined)
            ORDER BY month
        """)
        formatted_org_growth = [
            {'month': row[0], 'count': row[1]}
            for row in cursor.fetchall()
        ]

    context = {
        'total_students': total_students,
        'total_orgs': total_orgs,
        'total_members': total_members,
        'total_programs': total_programs,
        'monthly_registrations': json.dumps(formatted_registrations),
        'college_stats': json.dumps(college_stats),
        'program_stats': json.dumps(program_stats),
        'org_trends': json.dumps(org_trends),
        'monthly_org_growth': json.dumps(formatted_org_growth)
    }
    return render(request, 'dashboard.html', context)

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        return Student.objects.select_related('program', 'program__college').all()

class ProgramListView(ListView):
    model = Program
    template_name = 'program_list.html'
    context_object_name = 'programs'
    paginate_by = 10

    def get_queryset(self):
        return Program.objects.select_related('college').prefetch_related(
            'student_set'
        ).annotate(
            student_count=Count('student')
        ).all()

class CollegeListView(ListView):
    model = College
    template_name = 'college_list.html'
    context_object_name = 'colleges'
    paginate_by = 10

    def get_queryset(self):
        return College.objects.prefetch_related(
            'program_set',
            'organization_set'
        ).annotate(
            program_count=Count('program', distinct=True),
            student_count=Count('program__student', distinct=True)
        ).all()

class OrganizationListView(ListView):
    model = Organization
    template_name = 'org_list.html'
    context_object_name = 'organizations'
    paginate_by = 10

    def get_queryset(self):
        return Organization.objects.select_related('college').prefetch_related(
            'orgmembers_set'
        ).annotate(
            member_count=Count('orgmembers')
        ).all()

class OrgmemberListView(ListView):
    model = Orgmembers
    template_name = 'orgmem_list.html'
    context_object_name = 'orgmembers'
    paginate_by = 10

    def get_queryset(self):
        return Orgmembers.objects.select_related(
            'student',
            'organization',
            'organization__college'
        ).all()

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
