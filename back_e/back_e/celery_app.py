
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back_e.settings")

app = Celery("back_e")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.on_after_finalize.connect
def debug_registered_tasks(sender, **kwargs):
    print(f"[CELERY] Registered tasks: {sender.tasks.keys()}")

