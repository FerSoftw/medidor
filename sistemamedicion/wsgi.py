"""
WSGI config for admincaja project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys
from pathlib import Path
import environ

# find and activate virtualenv
base_dir=Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(base_dir, '.env'))
env = environ.Env()

activate_this = env('ACTIVATE_THIS_PATH')
if os.path.isfile(activate_this) and activate_this!=None and activate_this!='' and activate_this.endswith('activate_this.py'):
    exec(open(activate_this).read(), dict(__file__=activate_this))
   
from django.core.wsgi import get_wsgi_application

sys.path.append(str(base_dir))

os.environ["PYTHON_EGG_CACHE"]=os.path.join(base_dir, 'egg_cache')
os.environ["DJANGO_SETTINGS_MODULE"] = "sistemamedicion.settings"

from wsgicors import CORS


allowed_cors=env.list('ALLOWED_CORS')

application = CORS(get_wsgi_application(), headers="*", methods="*", maxage="180", origin=" ".join(allowed_cors))