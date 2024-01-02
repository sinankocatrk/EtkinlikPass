from channels.generic.websocket import AsyncWebsocketConsumer
import json
import django
from django.utils import timezone
from django.template.defaultfilters import date as _date
from channels.db import database_sync_to_async

class Consumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.advert_id = self.scope['url_route']['kwargs']['advert_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        self.room_group_name = f'chat_{self.advert_id}'

        # Gruba katıl
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Gruptan ayrıl
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # WebSocket'ten bir mesaj aldığınızda
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message == '':
            return

        inbox = await self.get_or_create_inbox(self.advert_id, self.user_id)
        db_message = await self.save_message(inbox, message)

        # Grubun tamamına mesaj gönder
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender_id': db_message.sender.id,
                'current_user_id': self.scope['user'].id,
                'username': db_message.sender.username,
                'message': message,
                'profilePicUrl': db_message.sender.profile_photo.url if db_message.sender.profile_photo else None,
                'time': _date(timezone.localtime(db_message.created_at), "SHORT_DATETIME_FORMAT")
            }
        )

    # Grup mesajı işleyici
    async def chat_message(self, event):

        sender_id = event['sender_id']
        current_user_id = event['current_user_id']
        username = event['username']
        message = event['message']
        profilePicUrl = event['profilePicUrl']
        time = event['time']

        # WebSocket'e mesaj gönder
        await self.send(text_data=json.dumps({
            'sender_id': sender_id,
            'current_user_id': current_user_id,
            'username': username,
            'message': message,
            'profilePicUrl': profilePicUrl,
            'time': time,
        }))


    @database_sync_to_async
    def get_or_create_inbox(self, advert_id, user_id):
        from advert.models import Advert
        from user.models import CustomUser
        from chat.models import Inbox

        advert = Advert.objects.get(id=advert_id)
        user = CustomUser.objects.get(id=user_id)
        receiver = advert.author
        inbox, created = Inbox.objects.get_or_create(advert=advert, sender=user, receiver=receiver)
        return inbox


    @database_sync_to_async
    def save_message(self, inbox, message_text):
        from chat.models import Message
        from user.models import CustomUser

        

        user = CustomUser.objects.get(id=self.scope['user'].id)
        message = Message.objects.create(inbox=inbox, sender=user, content=message_text, created_at=django.utils.timezone.now())

        inbox.last_message = message
        inbox.updated_at = django.utils.timezone.now()

        inbox.save()

        return message
