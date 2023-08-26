from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProjectSerializer
from base.models import Projects, Tag
from users.models import Profile
from rest_framework.permissions import IsAuthenticated, IsAdminUser

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'GET':'/api/projects/id/vote'},

        {'GET':'/api/users/token'},
        {'GET':'/api/users/token/refresh'},
    ]

    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    projects = Projects.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request,pk):
    project = Projects.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)