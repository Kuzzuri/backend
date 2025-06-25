import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from message_app.models import Message
from user_app.models import User
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from django.utils import timezone




class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token_raw = self.scope["query_string"].decode()
        token = parse_qs(token_raw)['token'][0]
        access_token = AccessToken(token)
        self.user_id = access_token["user_id"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"chat_{self.room_name}"
        print("✅ WebSocket connected")
        await self.channel_layer.group_add(
            self.group_name,         
            self.channel_name        
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        messageType = text_data_json['type']
        group_id = text_data_json['group']
        user_obj = await self.get_user(self.user_id)
        group_obj = await self.get_user(group_id)
        if(messageType == 'chat'):
            await self.post_message(sender=user_obj, reciever=group_obj, message_body=message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    'user': self.user_id
                }
            )
        elif(messageType == 'typing'):
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_typing",
                    'user': self.user_id
                }
            )
        
    @database_sync_to_async
    def get_user(self, user_id):
        return get_object_or_404(User, id=user_id)
    @database_sync_to_async
    def post_message(self, sender, reciever, message_body):
        return Message.objects.create(sender=sender, reciever=reciever, message_body=message_body)
    
    async def chat_message(self, event):
        message = event["message"]
        user = event['user']
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": message,
            'user': user
        }))
    async def chat_typing(self, event):
        user = event['user']
        await self.send(text_data=json.dumps({
            "type": "typing",
            'user': user
        }))

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token_string = self.scope['query_string'].decode()
        access_token = AccessToken(token_string)
        token = access_token['user_id']
        self.user = await self.get_user(token)
        await self.user_online(self.user)
        await self.accept()
        await self.send(
            text_data= json.dumps(
                {'type': 'connection_established'}
            )
        )
    async def disconnect(self, code):
        await self.user_offline(self.user)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        lat = text_data_json['lat']
        lon = text_data_json['lon']
        location = f'{lat},{lon}'
        await self.set_location(self.user, location)
    @database_sync_to_async
    def get_user(self, user_id):
        return get_object_or_404(User, id=user_id)
    @database_sync_to_async
    def user_online(self, user):
        user.online = True
        user.save()
    @database_sync_to_async
    def user_offline(self, user):
        user.online = False
        user.last_online = timezone.now()
        user.save()
    @database_sync_to_async
    def set_location(self, user, location):
        user.location = location
        user.save()
        
        
        
        
