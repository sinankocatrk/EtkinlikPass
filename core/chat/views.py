import datetime
from django.shortcuts import get_object_or_404, redirect, render
import json
from django.db.models.functions import Cast
from django.db.models import CharField

from advert.models import Advert
from user.models import CustomUser
from .models import Inbox, Message
from django.utils import timezone
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import date as _date

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return _date(o, "SHORT_DATETIME_FORMAT")
        return super().default(o)

def chat_index(request):
    return render(request, 'index.html')

def chat_room(request, advert_id, user_id):
    inbox = get_or_create_chat(advert_id, user_id)

    all_messages = Message.objects.filter(inbox=inbox)
    current_user = CustomUser.objects.get(id=request.user.id)
    for message in all_messages:
        if message.sender != current_user and message.is_read is False:
            print(message.content, message.sender.username, current_user.username)
            message.is_read = True
            message.save()

    old_messages = Message.objects.filter(inbox=inbox).annotate(
    formatted_date=Cast('created_at', CharField())
    ).values('sender__id', 'sender__username', 'content', 'created_at')

    i=0
    for message in old_messages:
        message['created_at'] = _date(timezone.localtime(message['created_at']), "SHORT_DATETIME_FORMAT")
        message['profile_photo_url'] = all_messages[i].sender.profile_photo.url if all_messages[i].sender.profile_photo else None
        i += 1

    old_messages_json = json.dumps(list(old_messages), cls=CustomJSONEncoder)

    current_user_id = request.user.id

    context = {
        'inbox': inbox,
        'advert_id': advert_id,
        'user_id': user_id,
        'old_messages_json': old_messages_json,
        'current_user_id': current_user_id,
    }

    return render(request, 'chat/chat.html', context)

def inbox(request):

    user = CustomUser.objects.get(id=request.user.id)

    sender_inboxes = Inbox.objects.filter(sender=user)
    receiver_inboxes = Inbox.objects.filter(receiver=user)

    context = {
        'sender_inboxes': sender_inboxes,
        'receiver_inboxes': receiver_inboxes,
        'current_user': user,
    }

    return render(request, 'chat/inbox.html', context)


def get_or_create_chat(advert_id, user_id):

    if(not advert_id or not user_id):
        return redirect('core:index')
    
    advert = get_object_or_404(Advert, id=advert_id)
    user = get_object_or_404(CustomUser, id=user_id)

    inbox, created = Inbox.objects.get_or_create(advert=advert, sender=user, receiver=advert.author)

    return inbox