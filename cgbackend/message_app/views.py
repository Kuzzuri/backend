from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message
from .serializers import MessageSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q


class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        query = request.query_params.get('sender')
        if query is not None:
            queryset = Message.objects.filter(Q(sender=query) & Q(reciever=str(request.user.id)) | Q(sender=str(request.user.id)) & Q(reciever=query))
        else:
            queryset = Message.objects.filter(Q(sender=request.user) | Q(reciever=request.user))
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
