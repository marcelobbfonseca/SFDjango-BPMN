from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from ..models import Sequence
from ..forms import SequenceForm


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
