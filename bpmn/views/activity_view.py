from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from ..models import Activity
from ..forms import ActivityForm


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
