import json
from channels.generic.websocket import AsyncWebsocketConsumer
        
        
class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "payment_status"
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f"WebSocket closed with code: {close_code}")
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        

    async def send_payment_status(self, event):
        message = event['message']
        print("MESSAGE: ", message)
        await self.send(text_data=json.dumps({
            'message': message
        }))