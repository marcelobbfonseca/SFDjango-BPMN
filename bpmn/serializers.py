from rest_framework import serializers
from .models import Diagram, Process


class ProcessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Process
        fields = ('id', 'name', 'status')


class DiagramSerializer(serializers.HyperlinkedModelSerializer):

    process = ProcessSerializer(read_only = True)
    
    class Meta:
        model = Diagram
        fields = ('id', 'name', 'xml', 'svg', 'process')
