from os import name
from bs4 import BeautifulSoup
from django.contrib.auth.models import Group
from bpmn.models import (ProcessType, Activity, ActivityType,
    Pool, Lane, Event, Sequence, Flow)
# laneSet(pool), lane, activity, flow, gateway, event
class DiagramParserUtils:

    def __init__(self, diagram_xml) -> None:
        #TODO refactor ontology
        self.groups_map = {
            'editor_01':'Editor',
            'editor_chefe_01':'Editor chefe',
            'chefe_de_redacao_01':'Chefe de redação',
            'reporter_01':'Reporter'
        }

        content = []
        if(diagram_xml == 'file'):
            with open(diagram_xml, "r") as file:
                self.diagram_xml = file.readlines()
        else:
            self.diagram_xml = diagram_xml
        content = "".join(self.diagram_xml)
        self.bs_content = BeautifulSoup(content, "lxml")
        # self.bs_content = BeautifulSoup(content, "html.parser")


    def parse_diagram_xml(self):
        process = self.bs_content.find('bpmn:process')

        pools = self.create_pools()
        lanes = []
        for pool in pools:
            pool_lanes = self.create_lanes(pool)
            lanes = lanes + pool_lanes

        activities, activity_types = [], []
        for lane in lanes:
            lane_activities, lane_activity_types = self.create_activities(lane)
            activities = activities + lane_activities
            activity_types = activity_types + lane_activity_types

        events = self.create_events(process)
        sequences, flows = self.create_sequences()
        process_type = self.create_process_type(process)

        # import pdb;pdb.set_trace()
        print('alo')
        return pools, lanes, activities, activity_types, events
        
    def create_pools(self):
        lane_sets = self.bs_content.find_all('bpmn:laneset')
        if len(lane_sets) == 0:
            lane_sets.append(self.bs_content.find('bpmn:laneset'))
        participant = self.bs_content.find('bpmn:participant') # TODO testar com mais de 1 pool
        pools = []
        for lane_set in lane_sets:
            pools.append(Pool.objects.create(name=participant.get('name')))
        return pools


    def create_lanes(self, pool):
        process = self.get_bs_process()
        first_lane = process.find('bpmn:lane')
        diagram_lanes = first_lane.find_next_siblings()
        diagram_lanes.append(first_lane)
        lanes = []
        for lane in diagram_lanes:
            name = lane.get('name')
            group = Group.objects.get(name=self.groups_map[name])
            lanes.append(Lane.objects.create(name=name, pool=pool, responsable=group))
        return lanes


    def create_activities(self, lane):
        process = self.get_bs_process()
        tasks = process.find_all('bpmn:task')
        activity_types, activities = [], []
        for task in tasks:
            atype = ActivityType.objects.create(name=task.get('name'), lane=lane)
            activity = Activity.objects.create(type=atype)
            activity_types.append(atype)
            activities.append(activity)
        return activities, activity_types

    def create_sequences(self):
        process = self.get_bs_process()
        exclusive_gates = process.find_all('bpmn:exclusivegateway')
        sequences_flow = process.find_all('bpmn:sequenceflow')
        sequences, flows = [], []

        for sequence_flow in sequences_flow:
            sequence = Sequence()
            # import pdb;pdb.set_trace()
            source, s_type = self.identify_and_find(sequence_flow.get('sourceref'))
            target, t_type = self.identify_and_find(sequence_flow.get('targetref'))
            
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


    def create_events(self):
        process = self.get_bs_process()
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


    def identify_and_find(self, element):
        if element.split("_")[0] == "Activity":
            return ActivityType.objects.get(diagram_id=element), "Activity"
        elif element.split("_")[0] == "Gateway":
            return False
        
        # import pdb; pdb.set_trace()
        return Event.objects.get(diagram_id=element), "Event"

    def get_bs_process(self):
        return self.bs_content.find('bpmn:process')
