from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FriendSerializer, FriendRequestSerializer, FriendsSerializer
from .models import Friend, FriendRequest
from user_app.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q


class FriendView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        if request.user.is_superuser:
            queryset = Friend.objects.all()
            serializer = FriendSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = get_object_or_404(Friend, user_id=request.user.id)
            serializer = FriendSerializer(queryset)
            return Response(serializer.data)
    def patch(self, request):
        action = request.data.pop("action")
        user = request.user.id
        friend = request.data["friend_ids"][0]
        Friend.objects.get_or_create(user_id=user)
        Friend.objects.get_or_create(user_id=friend)
        queryset = get_object_or_404(Friend, user_id=user)
        friend_queryset = get_object_or_404(Friend, user_id=friend)
        serializer = FriendSerializer(queryset,data=request.data, partial=True)
        if action == "add":
            if serializer.is_valid():
                friend_queryset.friends.add(user)
                for i in queryset.friends.all():
                    queryset.friends.add(i.id)
                queryset.friends.add(friend)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        elif action == "remove":
            if serializer.is_valid():
                friend_queryset.friends.remove(user)
                for i in queryset.friends.all():
                    queryset.friends.add(i.id)
                queryset.friends.remove(friend)
                return Response({"detail: friend removed"})
        else:
            return Response({"detail: action not specified"})
        
class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        if request.user.is_superuser:
            queryset = FriendRequest.objects.all()
            serializer = FriendRequestSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            query = request.query_params.get('reciever')
            sonra_duzelt = request.query_params.get('sonra_duzelt')
            if query is not None:
                if sonra_duzelt is None:
                    queryset = FriendRequest.objects.filter(Q(sender=request.user.id) & Q(reciever=query))
                    serializer = FriendRequestSerializer(queryset, many=True)
                    return Response(serializer.data)
                elif sonra_duzelt is not None:
                    queryset = FriendRequest.objects.filter(reciever=query)
                    serializer = FriendsSerializer(queryset, many=True)
                    return Response(serializer.data)
            else:
                queryset = FriendRequest.objects.filter(Q(sender=request.user.id) | Q(reciever=request.user.id))
                serializer = FriendRequestSerializer(queryset, many=True)
                return Response(serializer.data)
    def post(self, request):
        if request.user.is_authenticated:
            serializer = FriendRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
    def delete(self, request):
        id = request.data.get('id')
        query = FriendRequest.objects.filter(id=id)
        query.delete()
        return Response({'deleted'})