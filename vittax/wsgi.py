import sys
path = '/home/dharanikumarnellore/VITTAX'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'vittax.settings'

application = get_wsgi_application()