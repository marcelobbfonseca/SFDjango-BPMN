from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from ..models import Lane
from ..forms import LaneForm

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
