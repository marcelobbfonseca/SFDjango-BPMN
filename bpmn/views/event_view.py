from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from ..models import Event
from ..forms import EventForm


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
