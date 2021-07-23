from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from ..models import Flow
from ..forms import FlowForm


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
