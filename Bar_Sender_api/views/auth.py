from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from Bar_Sender_api.models import MyUser, AccountType, account_type, my_user


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login User"""
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        my_user = MyUser.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
            'MyUser': my_user.id,
            'account_type': my_user.account_type.id
        }
        return Response(data)

    else:
        data = {
            'valid': False
        }

        return Response(data)

# apiview sets up what methods it will take


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
    )

    my_user = MyUser.objects.create(
        bio=request.data['bio'],
        user=new_user,
        accountType=request.data['account_type']
    )

    token = Token.objects.create(user=my_user.user)

    data = {
        'token': token.key,
        'userId': my_user.id,
        'accountType': account_type.id
    }

    return Response(data)
