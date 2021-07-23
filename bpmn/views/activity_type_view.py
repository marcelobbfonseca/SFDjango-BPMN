from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from ..models import ActivityType
from ..forms import ActivityTypeForm


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
