from django.db.models import Q

from chat.models import Inbox, Message
from user.models import CustomUser

def unread_message_count(request):
    total_unread_count = 0
    if request.user.is_authenticated:
        total_unread_count = 0
        user = CustomUser.objects.get(id=request.user.id)
    else:
        total_unread_count = 0
        return {'unread_message_count': total_unread_count}
        
    all_inboxes = Inbox.objects.filter(Q(sender=user) | Q(receiver=user))

    for inbox in all_inboxes:
        all_messages = Message.objects.filter(inbox=inbox)
        for message in all_messages:
            if message.sender != user and message.is_read is False:
                total_unread_count += 1
    return {'unread_message_count': total_unread_count}

def current_user_cp(request):
    user = None
    if request.user.is_authenticated:
        user = CustomUser.objects.get(id=request.user.id)
    else:
        user = None

    print("current_user_cp")
    return {'current_user_cp': user}