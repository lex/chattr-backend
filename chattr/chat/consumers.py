from datetime import datetime, timezone
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

# pretty easy to add support for more chat channels?
GROUP_NAME = 'chat'
MESSAGE_TYPE_NEW_MESSAGE = 'new_message'
MESSAGE_TYPE_CHATTER_JOINED = 'new_chatter'
MESSAGE_TYPE_UNDEFINED = 'undefined_message_type'


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
        message_type = content['message_type']
        name = content['name']
        message = content['message']
        timestamp = datetime.now(
            timezone.utc).isoformat().replace("+00:00", "Z")

        async_to_sync(self.channel_layer.group_send)(
            GROUP_NAME,
            {
                'type': MESSAGE_TYPE_NEW_MESSAGE if message_type == MESSAGE_TYPE_NEW_MESSAGE else
                (MESSAGE_TYPE_CHATTER_JOINED if message_type ==
                 MESSAGE_TYPE_CHATTER_JOINED else MESSAGE_TYPE_UNDEFINED),
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
            'message_type': MESSAGE_TYPE_NEW_MESSAGE,
            'name': name,
            'message': message,
            'timestamp': timestamp,
        })

    def new_chatter(self, event):
        name = event['name']
        timestamp = event['timestamp']

        self.send_json({
            'message_type': MESSAGE_TYPE_CHATTER_JOINED,
            'name': name,
            'timestamp': timestamp,
        })

    def undefined_message_type(self, event):
        print('something went wrong')
