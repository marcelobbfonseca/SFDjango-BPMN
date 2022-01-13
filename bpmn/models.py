from django.db import models
from django.contrib.auth.models import Group
from django.utils.html import format_html


POSSIBLE_EVENTS = [
    ('Start process', 'Start process'),
    ('End process', 'End process'),
]

PROCESS_POSSIBLE_STATUSES = [
    ('INITIALIZING', 'INITIALIZING'),
    ('ACTIVE', 'ACTIVE'),
    ('FINISHED', 'FINISHED'),
]

def change_name_casing(name):

    return ''.join([word.capitalize() for word in name.split()])

####################################### Type of structures (BASIC UNITS) #######################################

class ProcessType(models.Model):

    name = models.CharField(max_length=255, default='')
    flow = models.ForeignKey('Flow', on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Process Type'
        verbose_name_plural = 'Process Types'

    def __str__(self):

        return 'Process@' + change_name_casing(self.name)

class Flow(models.Model):

    sequences = models.ManyToManyField('Sequence')

    class Meta:

        verbose_name = 'Flow'
        verbose_name_plural = 'Flows'

    def __str__(self):

        return 'Flow@' + str(self.id)

class Pool(models.Model):

    name = models.CharField(max_length=255, default='')

    class Meta:

        verbose_name_plural = 'Pools'

    def __str__(self):
        return 'Pool@' + change_name_casing(self.name)

    def __repr__(self) -> str:
        # return super().__repr__()    
        return f"<Pool id: {self.id}, name: '{self.name}' >"


class Lane(models.Model):

    name = models.CharField(max_length=255, default='')
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, default=None)
    responsable = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)

    class Meta:

        verbose_name_plural = 'Lanes'

    def __str__(self):

        return 'Lane@' + change_name_casing(self.name)

class ActivityType(models.Model):

    name = models.CharField(max_length=255, default='')
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE, default=None)
    diagram_id = models.CharField(max_length=255, default='')

    class Meta:

        verbose_name = 'Activity Type'
        verbose_name_plural = 'Activity Types'

    def __str__(self):

        return 'Activity@' + change_name_casing(self.name) + ' '
        return f"<Act_Type id: {self.id}, name: '{self.name}', diagram_id: '{self.diagram_id}' >"

####################################### Instances of structures #######################################
    

class Process(models.Model):

    name = models.CharField(max_length=255, default='')
    type = models.ForeignKey(ProcessType, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=255, default=PROCESS_POSSIBLE_STATUSES[0][1])
    current = models.ForeignKey('Activity', on_delete=models.CASCADE, default=None, null=True, blank=True)

    class Meta:

        verbose_name_plural = 'Processes'

    def possible_actions(self):

        html = ''

        for index, act in enumerate(get_possible_activities(self)):

            html += '<a class="button" href="../admin/bpmn/process/update_process_/{}-{}">{}</a> &nbsp'.format(self.id, index, str(act))

        for index, evt in enumerate(get_possible_events(self)): 

            html += '<a class="button" style="background-color:#ff86c5;" href="../admin/bpmn/process/update_process_/{}-{}">{}</a> &nbsp'.format(self.id, evt.name, str(evt))

        return format_html(html)

    def save(self, update=False, *args, **kwargs):

        super().save(*args, **kwargs)

    def __str__(self):

        return self.type.name

class Activity(models.Model):

    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, default=None)
    class Meta:

        verbose_name_plural = 'Activities'

    def __str__(self):

        return str(self.type)

class Event(models.Model):

    name = models.CharField(max_length=255, choices=POSSIBLE_EVENTS, default='')
    diagram_id = models.CharField(max_length=255, default='')
    class Meta:

        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):

        return 'Event@' + change_name_casing(self.name)

class Sequence(models.Model):

    current_activity = models.ForeignKey(ActivityType, on_delete=models.CASCADE,
        related_name='current_act', blank=True, null=True)
    current_event = models.ForeignKey(Event, on_delete=models.CASCADE,
            related_name='current_evt', blank=True, null=True)
    next_activity_options = models.ManyToManyField(ActivityType, blank=True,
        related_name='next_acts_opts',)
    next_event_options = models.ManyToManyField(Event, blank=True,
        related_name='next_event_opts')

    class Meta:

        verbose_name_plural = 'Sequences'

    def get_current_state(self):

        return str(self.current_activity or self.current_event)

    def get_next_opts(self):
        return self.next_activities() + self.next_events()

    def next_activities(self):
        return [ activity.name for activity in self.next_activity_options.all()]

    def next_events(self):
        return [ event.name for event in self.next_event_options.all()]

    def __str__(self):
        return self.get_current_state() + ' --> ' + ' or '.join(self.get_next_opts())



class Diagram(models.Model):
    name = models.CharField(max_length=255, default='')
    xml = models.TextField(default='')
    svg = models.TextField(default='')
    process_type = models.OneToOneField(ProcessType, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    def __str__(self):
        return "Diagram %s" % self.name


class Ontology(models.Model):
    name = models.CharField(max_length=255, default='')
    prefix = models.CharField(max_length=255, default='')
    path_name = models.CharField(max_length=255, default='')
    
    def __str__(self):
        return "name:{}, prefix:{}".format(self.name, self.prefix)

    @staticmethod
    def have_prefix(rdf_node):
        return bool(rdf_node.count('#'))

    @staticmethod
    def remove_prefix(rdf_node):
        return rdf_node.split('#')[1]

    @staticmethod
    def remove_prefixes(rdf_nodes):
        result = [ rdf_node.split('#')[1] for rdf_node in rdf_nodes]
        return result


################################## Functions to manipulate process update ##################################





def get_process_init(process):

    flow = process.type.flow
    appearances = {}

    for seq in flow.sequences.all():

        for item in [seq.current_event] + [seq.current_activity] + \
            list(seq.next_activity_options.all()) + list(seq.next_event_options.all()):

            appearances[item] = [0, seq]

    for seq in flow.sequences.all():

        if seq.next_activity_options:

            for act in seq.next_activity_options.all():

                appearances[act][0] += 1

        if seq.next_event_options:

            for evt in seq.next_event_options.all():

                appearances[evt][0] += 1

    keys = list(appearances.keys())
    item = keys[0]
    min = appearances[item][0]
    
    for key in keys:

        if appearances[key][0] < min:

            min = appearances[key] = 0
            item = key

    return appearances[item][1]

def get_possible_activities(process):

    if process.current is None:

        return [] # process first action must be an event

    else:

        seq = Sequence.objects.get(current_activity=process.current.type)

    acts = list(seq.next_activity_options.all())

    return acts

def get_possible_events(process):

    if process.status == PROCESS_POSSIBLE_STATUSES[2][0]:

        return []

    if process.current is None:

        seq = get_process_init(process)

        return [seq.current_event]

    else:

        seq = Sequence.objects.get(current_activity=process.current.type)

    evts = list(seq.next_event_options.all())
    
    return evts
