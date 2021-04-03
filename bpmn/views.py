from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from .models import Activity, ActivityType, Process, ProcessType, Pool, Lane, Event, Sequence, Flow
from .forms import ActivityForm, ActivityTypeForm, ProcessForm, ProcessTypeForm
from .forms import PoolForm, LaneForm, EventForm, SequenceForm, FlowForm, ProcessUpdateForm


####################################### Activity type views #######################################

class ActivityTypeView(TemplateView):

    template_name = "bpmn/activity_type_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['activities'] = ActivityType.objects.order_by('name').all      
       
        return context

class ActivityTypeCreate(FormView):

    template_name = "bpmn/activity_type_create_form.html"
    form_class = ActivityTypeForm
    success_url = reverse_lazy('activity_type_list')

    def form_valid(self, form):

        self.object = form.save()
        
        return super().form_valid(form)

class ActivityTypeUpdate(UpdateView):

    model = ActivityType
    fields = ['name', 'lane']
    success_url = reverse_lazy('activity_type_list')
    template_name = "bpmn/activity_type_update_form.html"

class ActivityTypeDelete(DeleteView):

    model = ActivityType
    success_url = reverse_lazy('activity_type_list')
    template_name = "bpmn/activity_type_delete_confirmation.html"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)

####################################### Process type views #######################################

class ProcessTypeView(TemplateView):

    template_name = "bpmn/process_type_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['processes'] = ProcessType.objects.order_by('name').all      
       
        return context

class ProcessTypeCreate(FormView):

    template_name = "bpmn/process_type_create_form.html"
    form_class = ProcessTypeForm
    success_url = reverse_lazy('process_type_list')

    def form_valid(self, form):

        self.object = form.save()
        
        return super().form_valid(form)

class ProcessTypeUpdate(UpdateView):

    model = ProcessType
    fields = ['name', 'flow']
    success_url = reverse_lazy('process_type_list')
    template_name = "bpmn/process_type_update_form.html"

class ProcessTypeDelete(DeleteView):

    model = ProcessType
    success_url = reverse_lazy('process_type_list')
    template_name = "bpmn/process_type_delete_confirmation.html"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)

####################################### Pool views #######################################

class PoolView(TemplateView):

    template_name = "bpmn/pool_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['pools'] = Pool.objects.order_by('name').all      
       
        return context

class PoolCreate(FormView):

    template_name = "bpmn/pool_create_form.html"
    form_class = PoolForm
    success_url = reverse_lazy('pool_list')

    def form_valid(self, form):

        self.object = form.save()
        
        return super().form_valid(form)

class PoolUpdate(UpdateView):

    model = Pool
    fields = ['name']
    success_url = reverse_lazy('pool_list')
    template_name = "bpmn/pool_update_form.html"

class PoolDelete(DeleteView):

    model = Pool
    success_url = reverse_lazy('pool_list')
    template_name = "bpmn/pool_delete_confirmation.html"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)

####################################### Lane views #######################################

class LaneView(TemplateView):

    template_name = "bpmn/lane_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['lanes'] = Lane.objects.order_by('name').all      
       
        return context

class LaneCreate(FormView):

    template_name = "bpmn/lane_create_form.html"
    form_class = LaneForm
    success_url = reverse_lazy('lane_list')

    def form_valid(self, form):

        self.object = form.save()
        
        return super().form_valid(form)

class LaneUpdate(UpdateView):

    model = Lane
    form_class = LaneForm
    success_url = reverse_lazy('lane_list')
    template_name = "bpmn/lane_update_form.html"

class LaneDelete(DeleteView):

    model = Lane
    success_url = reverse_lazy('lane_list')
    template_name = "bpmn/lane_delete_confirmation.html"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)

####################################### Event views #######################################

class EventView(TemplateView):

    template_name = "bpmn/event_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.order_by('name').all      
       
        return context

class EventCreate(FormView):

    template_name = "bpmn/event_create_form.html"
    form_class = EventForm
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):

        self.object = form.save()
        
        return super().form_valid(form)

class EventUpdate(UpdateView):

    model = Event
    fields = ['name']
    success_url = reverse_lazy('event_list')
    template_name = "bpmn/event_update_form.html"

class EventDelete(DeleteView):

    model = Event
    success_url = reverse_lazy('event_list')
    template_name = "bpmn/event_delete_confirmation.html"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)

####################################### Activity views #######################################

class ActivityView(TemplateView):

    template_name = "bpmn/activity_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = Activity.objects.order_by('type').all      
       
        return context

class ActivityCreate(FormView):

    template_name = "bpmn/activity_create_form.html"
    form_class = ActivityForm
    success_url = reverse_lazy('activity_list')

    def form_valid(self, form):

        self.object = form.save()
        
        return super().form_valid(form)

class ActivityUpdate(UpdateView):

    model = Activity
    fields = ['type']
    success_url = reverse_lazy('activity_list')
    template_name = "bpmn/activity_update_form.html"

class ActivityDelete(DeleteView):

    model = Activity
    success_url = reverse_lazy('activity_list')
    template_name = "bpmn/activity_delete_confirmation.html"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)

####################################### Sequence views #######################################

class SequenceView(TemplateView):

    template_name = "bpmn/sequence_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['sequences'] = Sequence.objects.order_by('current_activity').all      
       
        return context

class SequenceCreate(FormView):

    template_name = "bpmn/sequence_create_form.html"
    form_class = SequenceForm
    success_url = reverse_lazy('sequence_list')

    def form_valid(self, form):

        self.object = form.save()
        
        return super().form_valid(form)

class SequenceUpdate(UpdateView):

    model = Sequence
    fields = ['current_activity', 'current_event', 'next_activity_options', 'next_event_options']
    success_url = reverse_lazy('sequence_list')
    template_name = "bpmn/sequence_update_form.html"

class SequenceDelete(DeleteView):

    model = Sequence
    success_url = reverse_lazy('sequence_list')
    template_name = "bpmn/sequence_delete_confirmation.html"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)

####################################### Flow views #######################################

class FlowView(TemplateView):

    template_name = "bpmn/flow_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['flows'] = Flow.objects.order_by('id')     
       
        return context

class FlowCreate(FormView):

    template_name = "bpmn/flow_create_form.html"
    form_class = FlowForm
    success_url = reverse_lazy('flow_list')

    def form_valid(self, form):

        self.object = form.save()
        
        return super().form_valid(form)

class FlowUpdate(UpdateView):

    model = Flow
    fields = ['sequences']
    success_url = reverse_lazy('flow_list')
    template_name = "bpmn/flow_update_form.html"

class FlowDelete(DeleteView):

    model = Flow
    success_url = reverse_lazy('flow_list')
    template_name = "bpmn/flow_delete_confirmation.html"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)

####################################### Process views #######################################

class ProcessView(TemplateView):

    template_name = "bpmn/process_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['processes'] = Process.objects.order_by('type').all 
       
        return context

class ProcessModelingView(TemplateView):
    template_name = "bpmn/process_modeling.html"
    

class ProcessCreate(FormView):

    template_name = "bpmn/process_create_form.html"
    form_class = ProcessForm
    success_url = reverse_lazy('process_list')

    def form_valid(self, form):

        self.object = form.save()
        
        return super().form_valid(form)

class ProcessUpdate(UpdateView):

    model = Process
    form_class = ProcessUpdateForm
    success_url = reverse_lazy('process_list')
    template_name = "bpmn/process_update_form.html"

class ProcessDelete(DeleteView):

    model = Process
    success_url = reverse_lazy('process_list')
    template_name = "bpmn/process_delete_confirmation.html"

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)
