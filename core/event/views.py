import requests
from .models import Event
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def fetch_and_save_events(request):

    api_url = 'https://backend.etkinlik.io/api/v2/events'
    api_key = '75c4e94ee1237987fdfee2aa6a1048bf'

    params = {
        'take': 9999,
        'format_ids' : '19',
    }
    headers = {
        'X-Etkinlik-Token': api_key
    }

    response = requests.get(api_url, params=params, headers=headers)

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
