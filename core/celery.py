import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from task.tasks import remove_complete_task
    print('setup periodic tasks')
    sender.add_periodic_task(10, remove_complete_task.s(), name='remove_complete_task')