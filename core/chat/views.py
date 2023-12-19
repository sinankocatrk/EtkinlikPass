from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
import json
from django.db.models.functions import Cast
from django.db.models import CharField

from advert.models import Advert
from user.models import CustomUser
from .models import Inbox, Message


def chat_index(request):
    return render(request, 'index.html')

def chat_room(request, advert_id, user_id):
    inbox = get_or_create_chat(advert_id, user_id)

    all_messages = Message.objects.filter(inbox=inbox)
    for message in all_messages:
        if message.sender is not request.user and message.is_read is False:
            message.is_read = True
            message.save()

    # Kullanıcının ait olduğu Inbox'ın eski mesajlarını al
    old_messages = Message.objects.filter(inbox=inbox).annotate(
        formatted_date=Cast('created_at', CharField())
    ).values('sender__id', 'sender__username', 'content', 'formatted_date')

    old_messages_json = json.dumps(list(old_messages))

    current_user = CustomUser.objects.get(id=request.user.id)

    context = {
        'inbox': inbox,
        'advert_id': advert_id,
        'user_id': user_id,
        'old_messages_json': old_messages_json,
        'current_user': current_user,
    }

    return render(request, 'chat/chat.html', context)

def inbox(request):

    user = CustomUser.objects.get(id=request.user.id)

    sender_inboxes = Inbox.objects.filter(sender=user)
    receiver_inboxes = Inbox.objects.filter(receiver=user)

    context = {
        'sender_inboxes': sender_inboxes,
        'receiver_inboxes': receiver_inboxes,
    }

    return render(request, 'chat/inbox.html', context)


def get_or_create_chat(advert_id, user_id):

    if(not advert_id or not user_id):
        return redirect('core:index')
    
    advert = get_object_or_404(Advert, id=advert_id)
    user = get_object_or_404(CustomUser, id=user_id)

    inbox, created = Inbox.objects.get_or_create(advert=advert, sender=user, receiver=advert.author)

    return inbox