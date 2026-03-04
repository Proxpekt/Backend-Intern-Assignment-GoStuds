from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsCreatorOrReadOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    
    serializer_class = ProjectSerializer
    
    # Permission logic:
    # - Anyone can read (GET)
    # - Only authenticated users can create
    # - Only creator can update/delete
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my(self, request):
        projects = Project.objects.filter(creator=request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)