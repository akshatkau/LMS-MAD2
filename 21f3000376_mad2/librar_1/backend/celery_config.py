from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

CELERY_BEAT_SCHEDULE = {
    'generate_monthly_report': {
        'task': 'tasks.generate_monthly_report',
        'schedule': crontab(minute='*')
    },
    'daily_reminders': {
        'task': 'tasks.daily_reminders',
        'schedule': 20.0  
    }
}

celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE
