from rest_framework import serializers
from .models import Diagram, Process


class ProcessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Process
        fields = ('name', 'status')


class DiagramSerializer(serializers.HyperlinkedModelSerializer):

    process = ProcessSerializer(read_only = True)
    
    class Meta:
        model = Diagram
        fields = ('name','xml','svg', 'process')