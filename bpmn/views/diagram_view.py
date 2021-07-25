from rest_framework import viewsets
from ..models import Diagram
from ..serializers import DiagramSerializer


class DiagramViewset(viewsets.ModelViewSet):
    queryset = Diagram.objects.all()
    serializer_class = DiagramSerializer


