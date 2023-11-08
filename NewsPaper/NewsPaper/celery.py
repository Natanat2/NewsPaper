import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-weekly-newsletter': {
        'task': 'NewsPaper.tasks.send_weekly_article_list',
        'schedule': crontab(day_of_week = 'mon', hour = '8'),
        'options': {'queue': 'weekly-news'},
    },
}
