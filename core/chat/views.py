from django.shortcuts import get_object_or_404, redirect, render

from advert.models import Advert
from user.models import CustomUser
from .models import Inbox


def chat_index(request):
    return render(request, 'index.html')

def chat_room(request, advert_id, user_id):

    inbox = get_or_create_chat(advert_id, user_id)

    context = {
        'inbox': inbox,
        'advert_id': advert_id,
        'user_id': user_id
    }

    return render(request, 'chat/chat.html', context)

def get_or_create_chat(advert_id, user_id):

    if(not advert_id or not user_id):
        return redirect('core:index')
    
    advert = get_object_or_404(Advert, id=advert_id)
    user = get_object_or_404(CustomUser, id=user_id)

    inbox, created = Inbox.objects.get_or_create(advert=advert, sender=user, receiver=advert.author)

    return inbox