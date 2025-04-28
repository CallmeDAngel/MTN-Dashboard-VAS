from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# définir les paramètres par défaut de Django pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VAS_APP.settings')

app = Celery('VAS_APP')

# charger les configurations depuis Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-découverte des tâches définies dans les modules 'tasks.py'
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
