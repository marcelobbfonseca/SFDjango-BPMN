from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import Diagram
from ..serializers import DiagramSerializer
from django.http import JsonResponse
from bpmn.utils.diagram_parser_utils import DiagramParserUtils


class DiagramViewset(ModelViewSet):
    queryset = Diagram.objects.all()
    serializer_class = DiagramSerializer
    # def list retrieve create update/partial_update destroy 

    def create(self, request, format=None, *args, **kwargs):
        serializer = DiagramSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        diagram = serializer.save()
        
        parser = DiagramParserUtils(diagram.xml)
        diagram.process_type = parser.parse_diagram_xml_and_create_process()
        
        diagram.save()
        return JsonResponse(serializer.data)
        
    
    def list(self, request, format=None, *args, **kwargs):
        queryset = Diagram.objects.all().values('id', 'name', 'process_type', 'xml', 'svg')
        serializer = DiagramSerializer(queryset, many=True)
        return Response(serializer.data)