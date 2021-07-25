from .models import Diagram, Process
from rest_framework import serializers


class ProcessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Process
        fields = ('name', 'status')


class DiagramSerializer(serializers.HyperlinkedModelSerializer):

    process = ProcessSerializer(read_only = True)
    
    class Meta:
        model = Diagram
        fields = ('name','xml','svg', 'process')