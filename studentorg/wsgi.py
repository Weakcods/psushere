import os
import sys

# Add project directory to Python path
path = '/home/joshuawa/studentorg'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'studentorg.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
