import asyncio
import json
import channels

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            print(self.scope)
            user = await channels.auth.get_user(self.scope)
            print(self.scope['user'], "connected")
            print(user, "channels")
            await self.accept()

            self.joined_rooms = ['chatroom', "group2"]  #list should come from database
            for room in self.joined_rooms:
                await self.channel_layer.group_add(
                    'group_' + str(room),
                    self.channel_name
                )
        except Exception as e:
            print('error while connecting : ', e)

    async def disconnect(self, close_code):
        self.joined_rooms = ['chatroom']  #list should come from database
        for room in self.joined_rooms:
            await self.channel_layer.group_discard(
                'group_' + str(room),
                self.channel_name
        )
    
    async def receive(self, text_data):
        print(text_data, "from recieve")
        text_data_json = json.loads(text_data)

        group = text_data_json['group']
       
        message = text_data_json['message']
        username = text_data_json['username']
        userid = text_data_json['user_id']
        print(message)

        try:
            # now = datetime.now() need to send time dynamically.
            await self.channel_layer.group_send(
                'group_' + str(group),
                {
                    'type': 'chatroom_message',
                    's3_url_link': message, #TODO need to change message to presigned url
                    'to_group_id': group,
                    'created_at' : "dummytime",
                    'username': username,
                    'userid' : userid
                }
            )
            print("sent1")
        except Exception as e:
            print(e)

    async def chatroom_message(self, event):
        # self.room_name = 'test'
        # self.room_group_name = 'chat_test'
        try:
            message = event['s3_url_link']
            group = event['to_group_id']
            created_at = event['created_at']
            username = event['username']
            userid = event['userid']

            await self.send(text_data=json.dumps({
                's3_url_link': message, #TODO need to change message to presigned url
                'to_group_id': group,
                'created_at' : created_at,
                'username': username,
                'userid' : userid
            }))
            print("sent2")
        except Exception as e:
            
            print(e, "exception")


class ChatConsumer(channels.consumer.AsyncConsumer):
    """
    """
    async def websocket_connect(self, event):
        """
        """
        print("connected", event)

        self.user = self.scope["user"]
        other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        if other_user_id:
            other_user = await self.get_user(other_user_id)
        else:
            other_user = None

        if int(self.user.id) in [7, 8] and int(other_user_id) in [7, 8]:
            self.chat_room = "first_room"

        else:
            self.chat_room = "second_room"

        print("chat_room", self.chat_room)
        await self.channel_layer.group_add(
            self.chat_room, self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        """
        """
        print("receive", event)
        front_text = event.get("text", None)
        if front_text:
            dict_data = json.loads(front_text)
            msg = dict_data.get("message", "")

            if self.user.is_authenticated:
                username = f"{self.user.first_name} {self.user.last_name}"
            else:
                username = "Anonymous"

            response = {
                "message": msg,
                "username": username
            }

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(response)
                }
            )

    async def chat_message(self, event):
        """
        sends the actual message.
        """
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    async def websocket_disconnect(self, event):
        """
        """
        print("disconnect", event)

    @database_sync_to_async
    def get_user(self, user_id):
        """
        """
        return User.objects.get(id=user_id)
