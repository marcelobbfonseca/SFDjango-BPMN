from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from ..models import ProcessType
from ..forms import ProcessTypeForm



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

