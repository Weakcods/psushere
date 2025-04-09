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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('programs/', views.ProgramListView.as_view(), name='program-list'),
    path('colleges/', views.CollegeListView.as_view(), name='college-list'),
    path('organizations/', views.OrganizationListView.as_view(), name='organization-list'),
    path('orgmembers/', views.OrgmemberListView.as_view(), name='orgmember-list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
