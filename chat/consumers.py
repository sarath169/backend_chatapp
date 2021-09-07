import json
import channels

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            print(self.scope)
            user = await channels.auth.get_user(self.scope)
            print(self.scope['user'], "connected")
            print(user, "channels")
            await self.accept()

            self.joined_rooms = ['chatroom','group4', 'xyz']  #list should come from database
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
            print("sent2", "???")
        except Exception as e:
            
            print(e, "exception")