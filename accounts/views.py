from django.contrib.auth import login, logout
from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import LoginSerializer, UserSerializer, UserCreateSerializer


class AuthViewSet(viewsets.GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def get_permissions(self):
        if self.action in ('logout_user', 'get_session'):
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(methods=['post'], detail=False, url_path='login', serializer_class=LoginSerializer)
    def login_user(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, url_path='logout')
    def logout_user(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path='session', serializer_class=UserSerializer)
    def get_session(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class AuthWithTokenViewSet(viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ('logout_user', 'get_session'):
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(methods=['post'], detail=False, url_path='login', serializer_class=LoginSerializer)
    def login_user(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        key = user.token()
        return Response({"token": key})

    @action(methods=['delete'], detail=False, url_path='logout')
    def logout_user(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"message": "success"})

    @action(methods=['get'], detail=False, url_path='session', serializer_class=UserSerializer)
    def get_session(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
