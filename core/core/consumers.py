from channels.generic.websocket import AsyncWebsocketConsumer
import json

class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'  # Tüm kullanıcılar için ortak bir oda
        self.room_group_name = 'chat_%s' % self.room_name

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
