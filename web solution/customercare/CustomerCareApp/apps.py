from django.apps import AppConfig
import threading
import os

class CustomercareappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CustomerCareApp'
    def ready(self):
        # Avoid running the thread twice in development with auto-reload.
        if os.environ.get('RUN_MAIN') == 'true':
            from .views import emailgeneration
            email_thread = threading.Thread(target=emailgeneration, daemon=True)
            email_thread.start()