from django import forms
from .models import Activity, ActivityType, Process, ProcessType, Pool, Lane, Event, Sequence, Flow


class ActivityTypeForm(forms.ModelForm):

    class Meta:

        model = ActivityType
        fields = ['name', 'lane']
        labels = {'name' : 'Nome', 'lane' : 'Raia'}

class ProcessTypeForm(forms.ModelForm):

    class Meta:

        model = ProcessType
        fields = ['name', 'flow']
        labels = {'name' : 'Nome', 'flow' : 'Fluxo'}

class PoolForm(forms.ModelForm):

    class Meta:

        model = Pool
        fields = ['name']
        labels = {'name' : 'Nome'}

class LaneForm(forms.ModelForm):

    class Meta:

        model = Lane
        fields = ['name', 'pool', 'responsable']
        labels = {'name' : 'Nome', 'pool' : 'Pool', 'responsable' : 'Responsável'}

class EventForm(forms.ModelForm):

    class Meta:

        model = Event
        fields = ['name']
        labels = {'name' : 'Nome'}

class ActivityForm(forms.ModelForm):

    class Meta:

        model = Activity
        fields = ['type']
        labels = {'type' : 'Tipo de atividade'}

class SequenceForm(forms.ModelForm):

    class Meta:

        model = Sequence
        fields = ['current_activity', 'current_event', 'next_activity_options', 'next_event_options']
        labels = {'current_activity' : 'Atividade atual',
                  'current_event' : 'Evento atual',
                  'next_activity_options' : 'Próxima(s) atividade(s)',
                  'next_event_options' : 'Próximo(s) evento(s)'
                 }

class FlowForm(forms.ModelForm):

    class Meta:

        model = Flow
        fields = ['sequences']
        labels = {'sequences' : 'Sequências'}

class ProcessForm(forms.ModelForm):

    class Meta:

        model = Process
        fields = ['name', 'type', 'status', 'current']
        labels = {'name' : 'Nome', 'type' : 'Tipo', 'status' : 'Estado', 'current' : 'Atual'}

    def __init__(self, *args, **kwargs):
        
        super(ProcessForm, self).__init__(*args, **kwargs)
        
        self.fields['status'].disabled = True
        self.fields['current'].disabled = True

class ProcessUpdateForm(forms.ModelForm):

    class Meta:

        model = Process
        fields = ['name', 'type', 'status', 'current']
        labels = {'name' : 'Nome', 'type' : 'Tipo', 'status' : 'Estado', 'current' : 'Atual'}
        
    def __init__(self, *args, **kwargs):
        
        super(ProcessUpdateForm, self).__init__(*args, **kwargs)
        
        self.fields['type'].disabled = True
        self.fields['status'].disabled = True
        self.fields['current'].disabled = True