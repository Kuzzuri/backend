from django.db import models
from user_app.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_reciever')
    message_body = models.TextField(max_length=500)
    time_stamp = models.DateTimeField(auto_now_add=True)
