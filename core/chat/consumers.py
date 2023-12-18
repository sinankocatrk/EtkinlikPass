from channels.generic.websocket import AsyncWebsocketConsumer
import json
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

        # Inbox'ı bulun veya oluşturun
        inbox = await self.get_or_create_inbox(self.advert_id, self.user_id)

        # Mesajı veritabanına kaydedin
        await self.save_message(inbox, message)

        # Grubun tamamına mesaj gönder
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Grup mesajı işleyici
    async def chat_message(self, event):
        message = event['message']

        # WebSocket'e mesaj gönder
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_or_create_inbox(self, advert_id, user_id):
        from advert.models import Advert
        from user.models import CustomUser
        from chat.models import Inbox

        advert = Advert.objects.get(id=advert_id)
        user = CustomUser.objects.get(id=user_id)
        inbox, created = Inbox.objects.get_or_create(advert=advert, sender=user, receiver=advert.author)
        return inbox

    @database_sync_to_async
    def save_message(self, inbox, message_text):
        from chat.models import Message
        from user.models import CustomUser

        user = CustomUser.objects.get(id=self.scope['user'].id)
        return Message.objects.create(inbox=inbox, content=message_text, sender=user)
