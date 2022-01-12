from django.shortcuts import render
from rest_framework import serializers
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework import renderers, parsers, status
from rest_framework.response import Response
from client import views as client_views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# Create your views here.


class ProjectSerializer(serializers.ModelSerializer):
    tracking_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField(method_name='get_completion_rate')
    client_object = serializers.SerializerMethodField(method_name='get_client')
    
    class Meta:
        model = Project
        # fields = ['id', 'title', 'description', 'status', 'status_display', 'tracking_type_display', 'completion_rate']
        fields = '__all__'

    def get_client(self, instance):
        return client_views.ClientSerializer(instance.client, many=False).data

    def get_tracking_type_display(self, obj):
        return obj.get_tracking_type_display()

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_completion_rate(self, instance):
        completed = 0.0
        if instance.tracking_type == 'M':
            milestones = Milestone.objects.filter(project=instance).values('id')

            features = Feature.objects.filter(milestone_id__in=milestones).exclude(status=4)

            completed_features = features.filter(status=5)

            completed = (completed_features.count() / features.count()) * 100 if features.count() else 0.0

        elif instance.tracking_type == 'F':
            features = Feature.objects.filter(project=instance).exclude(status=4)

            completed_features = features.filter(status=5)

            completed = (completed_features.count() / features.count()) * 100 if features.count() else 0.0

        elif instance.tracking_type == 'C':
            checklist = CheckList.objects.filter(project=instance).exclude(status=4)

            completed_checklist = checklist.filter(status=5)

            completed = (completed_checklist.count() / checklist.count()) * 100 if checklist.count() else 0.0
        
        return round(completed, 2)


class Projects(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    parser_classes = [parsers.JSONParser]

    def get(self, request):

        projects = Project.objects.filter(created_by=request.user)

        serializer = ProjectSerializer(projects, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        client_id = request.data.get('client_id')
        tracking_type = request.data.get('tracking_type')

        project = Project.objects.create(
            title=title,
            description=description,
            client_id=client_id,
            tracking_type=tracking_type,
            status=0,
            created_by=request.user
        )

        serializer = ProjectSerializer(project, context={'request': request}, many=False) 
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectId(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    parser_classes = [parsers.JSONParser]

    def get(self, request, **kwargs):
        id = kwargs.get('id')

        project = None

        try:
            project = Project.objects.get(id=id)
        except:pass

        serializer = ProjectSerializer(project, context={'request': request}, many=False)

        return Response({'project': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        id = kwargs.get('id')

        project = None

        try:
            project = Project.objects.get(id=id)
        except:pass

        title = request.data.get('title')
        description = request.data.get('description')
        statuss = request.data.get('status')

        project.title = title
        project.description = description
        project.status = statuss

        project.save()

        serializer = ProjectSerializer(project, context={'request': request}, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ChecklistSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckList
        fields = '__all__'


class Checklists(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    parser_classes = [parsers.JSONParser]

    def get(self, request, **kwargs):
        id = kwargs.get('id')

        project = None

        try:
            project = Project.objects.get(id=id)
        except:pass

        checklists = CheckList.objects.filter(project=project)

        serializer = ChecklistSerializer(checklists, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        id = kwargs.get('id')

        project = None

        try:
            project = Project.objects.get(id=id)
        except:pass

        description = request.data.get('description')

        nc = CheckList.objects.create(project=project, description=description, created_by=request.user)

        serializer = ChecklistSerializer(nc, context={'request': request}, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, **kwargs):
        id = kwargs.get('id')

        checklist = None

        try:
            checklist = CheckList.objects.get(id=id)
        except:pass

        description = request.data.get('description')
        statuss = request.data.get('status')


        checklist.status = statuss
        checklist.description = description
        checklist.save()

        serializer = ChecklistSerializer(checklist, context={'request': request}, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields = '__all__'


class MilestoneSerializer(serializers.ModelSerializer):

    features = serializers.SerializerMethodField(method_name='get_features')
    completion_rate = serializers.SerializerMethodField(method_name='get_completion_rate')

    class Meta:
        model = Milestone
        fields = '__all__'

    def get_features(self, instance):
        features = Feature.objects.filter(milestone=instance)

        serializer = FeatureSerializer(features, many=True)

        return serializer.data

    def get_completion_rate(self, instance):
        # completed = 0.0
        # if instance.tracking_type == 'M':
        # milestones = Milestone.objects.filter(project=instance).values('id')

        features = Feature.objects.filter(milestone=instance).exclude(status=4)

        completed_features = features.filter(status=5)

        completed = (completed_features.count() / features.count()) * 100 if features.count() else 0.0

        return round(completed, 2)


class Milestones(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    parser_classes = [parsers.JSONParser]

    def get(self, request, **kwargs):
        id = kwargs.get('id')

        project = None

        try:
            project = Project.objects.get(id=id)
        except:pass

        milestones = Milestone.objects.filter(project=project)

        serializer = MilestoneSerializer(milestones, context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        id = kwargs.get('id')

        project = None

        try:
            project = Project.objects.get(id=id)
        except:pass

        description = request.data.get('description')

        nc = Milestone.objects.create(project=project, description=description, created_by=request.user)

        serializer = MilestoneSerializer(nc, context={'request': request}, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, **kwargs):
        id = kwargs.get('id')

        milestone = None

        try:
            milestone = Milestone.objects.get(id=id)
        except:pass

        description = request.data.get('description')
        # statuss = request.data.get('status')

        # checklist.status = statuss
        milestone.description = description
        milestone.save()

        serializer = MilestoneSerializer(milestone, context={'request': request}, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MilestoneFeatures(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    parser_classes = [parsers.JSONParser]

    def get(self, request, **kwargs):
        id = kwargs.get('id')

        milestone = None

        try:
            milestone = Milestone.objects.get(id=id)
        except:pass

        features = Feature.objects.filter(milestone=milestone)

        serializer = MilestoneSerializer(milestone, context={'request': request}, many=False)

        ferializer = FeatureSerializer(features, context={'request': request}, many=True)

        return Response({'milestone': serializer.data, 'features': ferializer.data}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        id = kwargs.get('id')
        description = request.data.get('description')
        milestone = None

        try:
            milestone = Milestone.objects.get(id=id)
        except:pass

        nf = Feature.objects.create(
            milestone=milestone,
            project=milestone.project,
            description=description,
            created_by=request.user
        )

        serializer = FeatureSerializer(nf, context={'request': request}, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, **kwargs):
        id = kwargs.get('id')

        feature = None

        try:
            feature = Feature.objects.get(id=id)
        except:pass

        description = request.data.get('description')
        statuss = request.data.get('status')

        feature.status = statuss
        feature.description = description
        feature.save()

        serializer = FeatureSerializer(feature, context={'request': request}, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)