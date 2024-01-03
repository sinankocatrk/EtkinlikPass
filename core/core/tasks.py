from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from django.utils import timezone


import requests

scheduler_started = False

API_KEY_FILE = 'keys/api.key'
SCHEDULER_LOG_FILE = 'logs/scheduler.log'

def load_api_key():
    with open(API_KEY_FILE, 'rb') as file:
        key = file.read()
    return key

api_key = load_api_key()

def fetch_and_save_events():
    from event.models import Event

    now = timezone.localtime(timezone.now())
    
    print(f"{now} - Fetching events...")

    api_url = 'https://backend.etkinlik.io/api/v2/events'

    params = {
        'take': 9999,
        'format_ids' : '19', # Konser
    }
    headers = {
        'X-Etkinlik-Token': api_key
    }

    response = requests.get(api_url, params=params, headers=headers)

    created_events = 0
    created_events_ids = []
    if response.status_code == 200:
        events_data = response.json().get('items', []) 

        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                id=event_data.get('id'),
                defaults={
                    'title': event_data.get('name'),
                    'location': event_data.get('venue', {}).get('name', ''),
                    'city': event_data.get('venue', {}).get('city', {}).get('name', ''),
                    'start_time': event_data.get('start'),
                    'description': event_data.get('content'),
                    'image_url': event_data.get('poster_url'),
                    'is_free': event_data.get('is_free', False),
                    'ticket_url': event_data.get('ticket_url', ''),
                }
            )

            if created:
                created_events += 1
                created_events_ids.append(event.id)
    
    with open(SCHEDULER_LOG_FILE, 'a') as file:
        file.write(f"|-| {now} - {created_events} new events added.\n")
        for event_id in created_events_ids:
            file.write(f"\t{event_id}\n")

    print(f"{datetime.now()} - {created_events} new events added.")

def remove_outdated_adverts_and_events():
    from advert.models import Advert
    from event.models import Event

    now = timezone.localtime(timezone.now())

    print(f"{now} - Removing outdated adverts and events...")

    

    all_adverts = Advert.objects.all()
    all_events = Event.objects.all()

    deleted_adverts_count = 0
    deleted_events_count = 0
    deleted_advert_ids = []
    deleted_event_ids = []
    for advert in all_adverts:
        if advert.is_deleted is False and advert.event.start_time < now:
            advert.is_deleted = True
            advert.deleted_at = now
            advert.event.is_deleted = True
            advert.event.deleted_at = now
            advert.event.save()
            advert.save()
            deleted_advert_ids.append(advert.id)
            deleted_event_ids.append(advert.event.id)
            deleted_adverts_count += 1
            deleted_events_count += 1
    
    for event in all_events:
        if event.is_deleted is False and event.start_time < now:
            event.is_deleted = True
            event.deleted_at = now
            event.save()
            deleted_event_ids.append(event.id)
            deleted_events_count += 1

    with open(SCHEDULER_LOG_FILE, 'a') as file:
        file.write(f"|-| {now} - {deleted_adverts_count} adverts deleted.\n")
        for advert_id in deleted_advert_ids:
            file.write(f"\t{advert_id}\n")
        file.write(f"|-| {now} - {deleted_events_count} events deleted.\n")
        for event_id in deleted_event_ids:
            file.write(f"\t{event_id}\n")
    
    print(f"{datetime.now()} - {deleted_adverts_count} adverts deleted.")
    print(f"{datetime.now()} - {deleted_events_count} events deleted.")


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_save_events, 'cron', hour=0, minute=0)
scheduler.add_job(remove_outdated_adverts_and_events, 'cron', hour='*')