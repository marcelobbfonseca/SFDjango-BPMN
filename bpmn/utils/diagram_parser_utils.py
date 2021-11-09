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
            lanes = lanes + pool_lanes

        activities, activity_types = [], []
        for lane in lanes:
            lane_activities, lane_activity_types = self.create_activities(lane, process)
            activities = activities + lane_activities
            activity_types = activity_types + lane_activity_types

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
        for lane_set in lane_sets:
            pools.append(Pool.objects.create(name=participant.get('name')))
        return pools


    def create_lanes(self, pool, process):
        diagram_lanes = process.find_all('bpmn:lane')
        lanes = []
        for lane in diagram_lanes:
            lanes.append(Lane.objects.create(name=lane.get('name'), pool=pool))
        return lanes


    def create_activities(self, lane, process):
        tasks = process.find_all('bpmn:task')
        activity_types, activities = [], []
        for task in tasks:
            type = ActivityType.objects.create(name=task.get('name'), lane=lane)
            activity = Activity.objects.create(type=type)
            activity_types.append(type)
            activities.append(activity)
        return activities, activity_types

    def create_sequences(self, process):
        exclusive_gates = process.find_all('bpmn:exclusivegateway')
        sequences_flow = process.find_all('bpmn:sequenceflow')
        sequences, flows = [], []

        for sequence_flow in sequences_flow:
            sequence = Sequence.new()

            source, s_type = self.identify_and_find(sequence_flow.get('sourceRef'))
            target, t_type = self.identify_and_find(sequence_flow.get('targetRef'))
            
            if s_type == "Activity":
                sequence.current_activity = source
            else:
                sequence.current_event = source
            if t_type == "event":
                sequence.current_activity = target
            else:
                sequence.current_event = target

            sequence.save()
            sequences.append(sequence)
        return sequences, flows


    def create_events(self, process):
        start_event = process.find('bpmn:startevent')
        end_event = process.find('bpmn:endevent')
        events = []
        if start_event:
            event = Event.objects.create(name='Inicio',diagram_id=start_event.get('id'))
            events.append(event)
        if end_event:
            event = Event.objects.create(name='Fim', diagram_id=end_event.get('id'))
            events.append(event)
        return events
        

    def create_process_type(self, process):
        pass


    def identify_and_find(element):
        if element.split("_")[0] == "Activity":
            return ActivityType.objects.get(diagram_id=element), "Activity"
        elif element.split("_")[0] == "Gateway":
            
            return False
        return Event.objects.get(diagram_id=element), "Event"