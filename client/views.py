from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework import renderers, parsers, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import serializers
from client.models import Client
from project.models import Project
from project.views import ProjectSerializer

# Create your views here.

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = '__all__'


class Clients(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    parser_classes = [parsers.JSONParser]

    def get(self, request):
        clients = Client.objects.filter(created_by=request.user)

        serializer = ClientSerializer(clients, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.data.get('name')
        kind = request.data.get('kind')
        contact = request.data.get('contact')
        email = request.data.get('email')

        cl = Client.objects.create(
            name=name,
            kind=kind,
            contact=contact,
            email=email,
            created_by=request.user
        )

        serializer = ClientSerializer(cl, context={'request': request}, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClientId(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    parser_classes = [parsers.JSONParser]

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        client = None
        try:
            client = Client.objects.get(id=id)
        except:pass

        projects = Project.objects.filter(client=client)

        serializer = ClientSerializer(client, context={'request': request}, many=False)

        perializer = ProjectSerializer(projects, context={'request': request}, many=True)

        return Response({'client': serializer.data, 'projects': perializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')

        client = None
        try:
            client = Client.objects.get(id=id)
        except:pass

        name = request.data.get('name')
        kind = request.data.get('kind')
        contact = request.data.get('contact')
        email = request.data.get('email')

        client.name = name
        client.kind = kind
        client.contact = contact
        client.email = email

        client.save()
        serializer = ClientSerializer(client, context={'request': request}, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)