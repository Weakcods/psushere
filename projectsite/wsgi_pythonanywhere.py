import os
import sys

# Add your project directory to the sys.path
path = '/home/joshettt/psuphere/psushere/projectsite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'projectsite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
