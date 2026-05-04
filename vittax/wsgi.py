import sys
path = '/home/dharanikumarnellore/VITTAX'
if path not in sys.path:
    sys.path.append(path)

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'vittax.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()