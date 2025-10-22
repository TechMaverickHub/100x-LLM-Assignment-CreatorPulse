import os
import threading

from django.apps import AppConfig


class MailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.mail'

    def ready(self):
        # Avoid running twice due to Django auto-reloader
        if os.environ.get("RUN_MAIN") != "true":
            return

        from app.mail.scheduler import start_scheduler
        threading.Thread(target=start_scheduler, daemon=True).start()
