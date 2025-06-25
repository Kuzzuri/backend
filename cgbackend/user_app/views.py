from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from .models import User
from django.db.models import Q

class UserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        user = request.user
        query = request.query_params.get('full_name')
        if user.is_authenticated:
            if user.is_superuser:
                queryset = User.objects.all()
                serializer = UserSerializer(queryset, many=True)
                return Response(serializer.data)
            elif (0 if query == None else len(query)) > 1:
                queryset = User.objects.all().filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
                serializer = UserSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                queryset = get_object_or_404(User, email=user)
                serializer = UserSerializer(queryset)
                return Response(serializer.data)
        else:
            return Response("kobe")
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def patch(self, request):
        user = request.user
        if user.is_authenticated:
            queryset = get_object_or_404(User, email=request.user)
            serializer = UserSerializer(queryset, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("not logged in")
    def delete(self, request):
        user = request.user
        if user.is_authenticated:
            if not user.is_superuser:
                user.delete()
                return Response({"detail": "User deleted."})
            else:
                return Response({"detail": "Admins cant delete users."})
        else:
            return Response("not logged in")

