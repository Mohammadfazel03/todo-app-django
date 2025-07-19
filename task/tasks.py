from celery import shared_task

from task.models import Task


@shared_task
def remove_complete_task():
    print('remove complete task')
    Task.objects.filter(is_complete__exact=True).delete()
