
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'run-monitoring-every-5-minutes': {
        'task': 'monitoring.tasks.run_monitoring_checks',
        'schedule': crontab(minute='*/5'),
    },
}
