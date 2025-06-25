from django.urls import path
from .views import FriendView, FriendRequestView

urlpatterns = [
    path('', FriendView.as_view()),
    path('request/', FriendRequestView.as_view())
]