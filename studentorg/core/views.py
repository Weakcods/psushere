from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = 'home.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class ComponentsView(TemplateView):
    template_name = 'components.html'

class FormsView(TemplateView):
    template_name = 'forms.html'

class TablesView(TemplateView):
    template_name = 'tables.html'

class NotificationsView(TemplateView):
    template_name = 'notifications.html'

class TypographyView(TemplateView):
    template_name = 'typography.html'

class IconsView(TemplateView):
    template_name = 'icons.html'
