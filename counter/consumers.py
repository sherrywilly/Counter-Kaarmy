from django.contrib.auth import get_user_model
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from counter.models import *

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def fetch_messages(self, data):
        _x = sync_to_async(Thread.objects.filter)(room__rid=data['room'])
        messages = await _x
        # print(messages)
        content = {
            'command': 'old',
            'messages': self.messages_to_json(messages)
        }
        # print(content)
        await self.send_message(content)

    async def new_messages(self, data):
        print('vljhvljh')
        author = data['from']
        print(author)
        auther_user = sync_to_async(User.objects.get)(username=author)
        x = await auther_user
        print(x.username)
        _xa = str(data['room'])
        room = sync_to_async(Room.objects.get)(rid=_xa)
        u = await room
        msg = sync_to_async(Thread.objects.create)(
            created_by_id=x.id,
            msg=data['message'],
            msg_type='1',
            room_id=u.id
        )
        message = await msg
        content = {
            'command': 'new_message',
            'message':  self.message_to_json({'author': x.username, 'content': message.msg, 'msg_type': message.msg_type, 'time': message.timestamp})
        }

        await self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []

        for msg in messages:
            print(msg)
            result.append(self.old_msg_to_json(msg))
        return result

    def old_msg_to_json(self, message):
        return{
            'author': message.created_by.username,
            'content': message.msg,
            'msg_type': message.msg_type,
            'timestamp': str(message.created_at)
        }

    def message_to_json(self, message):
        # print(message.author)
        return {
            'author': message.get('author'),
            'message': message.get('message'),
            'msg_type': message.get('msg_type'),
            'timestamp': str(message.get('time'))
        }
    commands = {
        'fetch_messages': fetch_messages,
        'new_messages': new_messages,
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        await self.commands[data['command']](self, data)
        # message = text_data_json['message']
        # user = text_data_json['user']
        # print(user)

    async def send_chat_message(self, message):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,

            }
        )

    async def send_message(self, message):
        print(message)
        await self.send(text_data=json.dumps(message))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': 'test',

        }))
