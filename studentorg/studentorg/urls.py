from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomepageView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('components/', views.ComponentsView.as_view(), name='components'),
    path('forms/', views.FormsView.as_view(), name='forms'),
    path('tables/', views.TablesView.as_view(), name='tables'),
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
    path('typography/', views.TypographyView.as_view(), name='typography'),
    path('icons/', views.IconsView.as_view(), name='icons'),
]
