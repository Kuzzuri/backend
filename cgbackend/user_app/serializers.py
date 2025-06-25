from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name  = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'first_name', 'last_name', 'email', 'is_premium', 'token_count', 'profile_image', 'password', 'last_online', 'location', 'online']
        extra_kwargs = {'password': {'write_only': True}}
    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserFriendSerializer(serializers.ModelSerializer):
    full_name  = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'is_premium', 'profile_image', 'location', 'online', 'last_online']
    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
