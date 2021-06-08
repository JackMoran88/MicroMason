import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicroMason.settings')

app = Celery('MicroMason')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-email-every-minutes': {
        'task': 'basepage.tasks.send_beat_email',
        'schedule': crontab()
    },
    'send-email-every-ten-minutes': {
        'task': 'basepage.tasks.np_update_invoice',
        'schedule': crontab(minute='*/10')
    },
}
