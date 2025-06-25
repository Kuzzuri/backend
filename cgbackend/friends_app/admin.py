from django.contrib import admin
from .models import Friend, FriendRequest

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'reciever', 'sent']
