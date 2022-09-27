from datetime import datetime, timezone
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

# pretty easy to add support for more chat channels?
GROUP_NAME = 'chat'


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            GROUP_NAME,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            GROUP_NAME,
            self.channel_name,
        )

    def receive_json(self, content):
        name = content['name']
        message = content['message']
        timestamp = datetime.now(
            timezone.utc).isoformat().replace("+00:00", "Z")

        async_to_sync(self.channel_layer.group_send)(
            GROUP_NAME,
            {
                'type': 'new_message',
                'name': name,
                'message': message,
                'timestamp': timestamp,
            }
        )

    def new_message(self, event):
        name = event['name']
        message = event['message']
        timestamp = event['timestamp']

        self.send_json({
            'name': name,
            'message': message,
            'timestamp': timestamp,
        })
