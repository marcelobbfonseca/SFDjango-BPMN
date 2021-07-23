from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from ..models import Pool
from ..forms import PoolForm


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

