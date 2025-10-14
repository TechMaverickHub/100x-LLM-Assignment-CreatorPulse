import threading

from django.apps import AppConfig


class MailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.mail'

    def ready(self):
        from app.mail.scheduler import start_scheduler
        threading.Thread(target=start_scheduler, daemon=True).start()
