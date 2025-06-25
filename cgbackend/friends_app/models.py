from django.db import models
from user_app.models import User

class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return self.user.email
    
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    sent = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ['sender', 'reciever']
