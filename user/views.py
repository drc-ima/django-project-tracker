from rest_framework.views import APIView
from rest_framework import renderers, parsers, status
from rest_framework.permissions import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
import datetime


class Signup(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    parser_classes = [parsers.JSONParser]
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')

        if first_name and last_name and username and email and password:
            pass
        else:
            return Response({'detail': 'Error! ensure all data fields are provided', 'code': '101'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(username=username)
            return Response({'detail': 'Username already exist', 'code': '102'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        new_user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        Token.objects.get_or_create(user=new_user)

        new_user.set_password(password)

        new_user.save()

        return Response({'detail': 'Successful', 'code': '100'}, status=status.HTTP_201_CREATED)


class Login(APIView):
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    parser_classes = [parsers.JSONParser]
    permission_classes = [AllowAny, ]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = authenticate(
                request=request, username=username, password=password)

            if user is None:
                return Response({'detail': 'Credentials do not match', 'code': '101'}, status=status.HTTP_400_BAD_REQUEST)

            elif user and not user.is_active:
                return Response({'detail': 'Your account is not active', 'code': '102'}, status=status.HTTP_400_BAD_REQUEST)

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            # print(token)

            return Response(
                {
                    "user": {
                        "token": token.key,
                        "first_name": user.first_name,
                        "username": user.username,
                        "last_name": user.last_name,
                        "email": user.email,
                        "full_name": user.get_full_name(),
                        "date_joined": datetime.datetime.strftime(user.date_joined, "%b.%Y")
                    },
                    'code': '100'
                }, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response({'detail': 'Something went wrong', 'code': '103'}, status=status.HTTP_400_BAD_REQUEST)
