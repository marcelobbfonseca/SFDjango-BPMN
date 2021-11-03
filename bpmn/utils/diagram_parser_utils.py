from os import name
from bs4 import BeautifulSoup
from bpmn.models import (ProcessType, Activity, ActivityType,
    Pool, Lane, Event, Sequence, Flow)
# laneSet(pool), lane, activity, flow, gateway, event
class DiagramParserUtils:

    def __init__(self, diagram_xml) -> None:
        content = []
        if(diagram_xml == 'file'):
            with open(diagram_xml, "r") as file:
                self.diagram_xml = file.readlines()
        else:
            self.diagram_xml = diagram_xml
        content = "".join(self.diagram_xml)
        self.bs_content = BeautifulSoup(content, "lxml")


    def parse_diagram_xml(self):
        process = self.bs_content.find('bpmn:process')

        pools = self.create_pools(self.bs_content)
        lanes = []
        for pool in pools:
            pool_lanes = self.create_lanes(pool, process)
            lanes.append(pool_lanes)

        activities, activity_types = self.create_activities(process)
        sequences, flows = self.create_sequences(process)
        events = self.create_events(process)
        process_type = self.create_process_type(process)

        import pdb;pdb.set_trace()
        print('alo')
        return pools, lanes, activities, activity_types, events
        
    def create_pools(self, content):
        lane_sets = content.find_all('bpmn:laneset')
        if len(lane_sets) == 0:
            lane_sets.append(content.find('bpmn:laneset'))
        participant = content.find('bpmn:participant') # testar com mais de 1 pool
        pools = []
        for lanse_set in lane_sets:
            pools.append(Pool.objects.create(name=participant.get('name')))
        return pools

    def create_lanes(self, pool, process):
        diagram_lanes = process.find_all('bpmn:lane')
        lanes = []
        for lane in diagram_lanes:
            lanes.append(Lane.objects.create(name=lane.get('name'), pool=pool))
        return lanes

    # mudar passando o process todo. precisa catar outras coisas
    def create_activities(self, process):
        tasks = process.find_all('bpmn:task')
        activity_types, activities = [], []
        for task in tasks:
            ActivityType.objects.create(name=task.get('name'), lane=1)
        return activities, activity_types

    def create_sequences(self, process):
        exclusive_gate = process.find_all('bpmn:exclusivegateway')
        sequences_flow = process.find_all('bpmn:sequenceflow')
        sequences, flows = [], []
        return sequences, flows


    def create_events(self, process):
        start_event = process.find('bpmn:startevent')
        end_event = process.find('bpmn:endevent')
        if start_event:
            Event.objects.create(name='Inicio')
        if end_event:
            Event.objects.create(name='Fim')


    def create_process_type(self, process):
        pass
