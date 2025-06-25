from rest_framework import serializers
from .models import Friend, FriendRequest
from user_app.models import User
from user_app.serializers import UserFriendSerializer
from django.shortcuts import get_object_or_404

class FriendSerializer(serializers.ModelSerializer):
    friends = UserFriendSerializer(many=True, read_only=True)
    friend_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True, source='friends'
    )
    class Meta:
        model = Friend
        fields = ['user', 'friends', 'friend_ids']
    
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'reciever', 'sent']

class FriendsSerializer(serializers.ModelSerializer):
    sender = UserFriendSerializer()
    reciever = UserFriendSerializer()

    class Meta:
        model = Friend
        fields = ['id', 'sender', 'reciever']
