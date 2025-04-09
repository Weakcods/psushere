import os
import sys

path = '/home/joshettt/psuphere/projectsite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'projectsite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
