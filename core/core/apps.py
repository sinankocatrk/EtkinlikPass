import sys
from django.apps import AppConfig
from .tasks import scheduler, scheduler_started, fetch_and_save_events, remove_outdated_adverts_and_events

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        if 'runserver' not in sys.argv:
            return
        
        global scheduler_started
        if not scheduler_started:
            print("Scheduler başlatılıyor...")
            fetch_and_save_events()
            remove_outdated_adverts_and_events()
            scheduler.start()
            scheduler_started = True
