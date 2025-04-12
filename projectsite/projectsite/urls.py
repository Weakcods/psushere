"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

handler404 = 'projectsite.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Student URLs
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student-add'),
    path('students/<int:pk>/', views.StudentUpdateView.as_view(), name='student-edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),
    
    # Program URLs
    path('programs/', views.ProgramListView.as_view(), name='program-list'),
    path('programs/add/', views.ProgramCreateView.as_view(), name='program-add'),
    path('programs/<int:pk>/', views.ProgramUpdateView.as_view(), name='program-edit'),
    path('programs/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program-delete'),
    
    # College URLs
    path('colleges/', views.CollegeListView.as_view(), name='college-list'),
    path('colleges/add/', views.CollegeCreateView.as_view(), name='college-add'),
    path('colleges/<int:pk>/', views.CollegeUpdateView.as_view(), name='college-edit'),
    path('colleges/<int:pk>/delete/', views.CollegeDeleteView.as_view(), name='college-delete'),
    
    # Organization URLs
    path('organizations/', views.OrganizationListView.as_view(), name='organization-list'),
    path('organizations/add/', views.OrganizationCreateView.as_view(), name='organization-add'),
    path('organizations/<int:pk>/', views.OrganizationUpdateView.as_view(), name='organization-edit'),
    path('organizations/<int:pk>/delete/', views.OrganizationDeleteView.as_view(), name='organization-delete'),
    
    # Orgmember URLs
    path('orgmembers/', views.OrgmemberListView.as_view(), name='orgmember-list'),
    path('orgmembers/add/', views.OrgmemberCreateView.as_view(), name='orgmember-add'),
    path('orgmembers/<int:pk>/', views.OrgmemberUpdateView.as_view(), name='orgmember-edit'),
    path('orgmembers/<int:pk>/delete/', views.OrgmemberDeleteView.as_view(), name='orgmember-delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
