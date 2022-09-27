from datetime import datetime, timezone
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

EVENT_TYPE_NEW_MESSAGE = 'new_message'


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.chat_channel_id = self.scope['url_route']['kwargs']['channel_id']
        async_to_sync(self.channel_layer.group_add)(
            self.chat_channel_id,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_channel_id,
            self.channel_name,
        )

    def receive_json(self, content):
        username = content.get('username', 'undefined')
        message = content.get('message', 'undefined')
        timestamp = datetime.now(
            timezone.utc).isoformat().replace("+00:00", "Z")

        async_to_sync(self.channel_layer.group_send)(
            self.chat_channel_id,
            {
                'type': EVENT_TYPE_NEW_MESSAGE,
                'username': username,
                'message': message,
                'timestamp': timestamp,
            }
        )

    def new_message(self, event):
        username = event['username']
        message = event['message']
        timestamp = event['timestamp']

        self.send_json({
            'username': username,
            'message': message,
            'timestamp': timestamp,
        })
