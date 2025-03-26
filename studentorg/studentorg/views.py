from django.shortcuts import render
from django.views.generic import ListView
from core.models import Organization  # Changed from studentorg.models to core.models

class HomepageView(ListView):  # Changed from OrganizationListView to HomepageView
    model = Organization
    template_name = 'home.html'
    context_object_name = 'home'