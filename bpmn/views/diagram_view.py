from rest_framework.viewsets import ModelViewSet
from ..models import Diagram
from ..serializers import DiagramSerializer
from django.http import JsonResponse
from rest_framework.response import Response

class DiagramViewset(ModelViewSet):
    queryset = Diagram.objects.all()
    serializer_class = DiagramSerializer
    # def list retrieve create update/partial_update destroy 

    def create(self, request, format=None, *args, **kwargs):
        serializer = DiagramSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        diagram = serializer.save()
        return JsonResponse(serializer.data)
        
    
    def list(self, request, format=None, *args, **kwargs):
        queryset = Diagram.objects.all().values('id', 'name', 'process')
        serializer = DiagramSerializer(queryset, many=True)
        return Response(serializer.data)