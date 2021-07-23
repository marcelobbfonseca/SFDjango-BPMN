from django.views.generic.base import TemplateView
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse
import json #, ast
from ..models import Process
from ..utils.process_utils import ProcessUtils
from ..utils.newsroom_process_utils import NewsroomProcessUtils
from ..forms import ProcessForm, ProcessUpdateForm
from rest_framework import generics


class ProcessView(TemplateView):

    template_name = "bpmn/process_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['processes'] = Process.objects.order_by('type').all 
       
        return context

class ProcessModelingView(TemplateView):
    template_name = "bpmn/process_modeling.html"
    
@method_decorator(csrf_exempt, name='dispatch')
class OntologySuggestionView(View):

    def post(self,request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        params = json.loads(body_unicode) # try
        result = {}

        newsroom_process_utils = NewsroomProcessUtils()
        if('elements' in params):
            laneTasks = ProcessUtils.get_tasks_by_lane(params['elements'])
        
            if(len(params['elements']['Lane'])):
                result['tasksStatuses'] = newsroom_process_utils.verify_tasks_by_lanes(laneTasks)

            # if('Participant' in params['elements']):
                # result['missing_tasks'] = newsroom_process_utils.verify_process_missing_tasks(laneTasks)
        return JsonResponse(result)



# @method_decorator(csrf_exempt, name='dispatch')
# class DiagramAPI(mixins.ListModelMixin,
#               mixins.CreateModelMixin):
#             #   generics.GenericAPIView):
#     model = Diagram
#     queryset = Diagram.objecst.all()


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
