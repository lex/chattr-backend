from datetime import datetime, timezone
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Channel, Message

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

        channel = Channel.objects.get(pk=self.chat_channel_id)
        m = Message.objects.create(
            username=username, message=message, channel=channel)
        m.save()

        async_to_sync(self.channel_layer.group_send)(
            self.chat_channel_id,
            {
                'type': EVENT_TYPE_NEW_MESSAGE,
                'username': m.username,
                'message': m.message,
                'timestamp': m.timestamp,
            }
        )

    def new_message(self, event):
        self.send_json({
            'username': event['username'],
            'message': event['message'],
            'timestamp': str(event['timestamp']),
        })
