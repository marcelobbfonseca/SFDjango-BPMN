from django.urls import path
from django.contrib.auth.views import LoginView
from .views.activity_view import *
from .views.activity_type_view import *
from .views.event_view import *
from .views.flow_view import *
from .views.lane_view import *
from .views.pool_view import *
from .views.process_type_view import *
from .views.process_view import *
from .views.sequence_view import *

urlpatterns = [
    path('', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('activity_type_list/', ActivityTypeView.as_view(), name='activity_type_list'),
    path('activity_type_create_form/', ActivityTypeCreate.as_view(), name='activity_type_create_form'),
    path('activity_type_update_form/<int:pk>', ActivityTypeUpdate.as_view(), name='activity_type_update_form'),
    path('activity_type_delete_confirmation/<int:pk>', ActivityTypeDelete.as_view(), name='activity_type_delete_confirmation'),
    path('process_type_list/', ProcessTypeView.as_view(), name='process_type_list'),
    path('process_type_create_form/', ProcessTypeCreate.as_view(), name='process_type_create_form'),
    path('process_type_update_form/<int:pk>', ProcessTypeUpdate.as_view(), name='process_type_update_form'),
    path('process_type_delete_confirmation/<int:pk>', ProcessTypeDelete.as_view(), name='process_type_delete_confirmation'),
    path('pool_list/', PoolView.as_view(), name='pool_list'),
    path('pool_create_form/', PoolCreate.as_view(), name='pool_create_form'),
    path('pool_update_form/<int:pk>', PoolUpdate.as_view(), name='pool_update_form'),
    path('pool_delete_confirmation/<int:pk>', PoolDelete.as_view(), name='pool_delete_confirmation'),
    path('lane_list/', LaneView.as_view(), name='lane_list'),
    path('lane_create_form/', LaneCreate.as_view(), name='lane_create_form'),
    path('lane_update_form/<int:pk>', LaneUpdate.as_view(), name='lane_update_form'),
    path('lane_delete_confirmation/<int:pk>', LaneDelete.as_view(), name='lane_delete_confirmation'),
    path('event_list/', EventView.as_view(), name='event_list'),
    path('event_create_form/', EventCreate.as_view(), name='event_create_form'),
    path('event_update_form/<int:pk>', EventUpdate.as_view(), name='event_update_form'),
    path('event_delete_confirmation/<int:pk>', EventDelete.as_view(), name='event_delete_confirmation'),
    path('activity_list/', ActivityView.as_view(), name='activity_list'),
    path('activity_create_form/', ActivityCreate.as_view(), name='activity_create_form'),
    path('activity_update_form/<int:pk>', ActivityUpdate.as_view(), name='activity_update_form'),
    path('activity_delete_confirmation/<int:pk>', ActivityDelete.as_view(), name='activity_delete_confirmation'),
    path('sequence_list/', SequenceView.as_view(), name='sequence_list'),
    path('sequence_create_form/', SequenceCreate.as_view(), name='sequence_create_form'),
    path('sequence_update_form/<int:pk>', SequenceUpdate.as_view(), name='sequence_update_form'),
    path('sequence_delete_confirmation/<int:pk>', SequenceDelete.as_view(), name='sequence_delete_confirmation'),
    path('flow_list/', FlowView.as_view(), name='flow_list'),
    path('flow_create_form/', FlowCreate.as_view(), name='flow_create_form'),
    path('flow_update_form/<int:pk>', FlowUpdate.as_view(), name='flow_update_form'),
    path('flow_delete_confirmation/<int:pk>', FlowDelete.as_view(), name='flow_delete_confirmation'),
    path('process_list/', ProcessView.as_view(), name='process_list'),
    path('process_create_form/', ProcessCreate.as_view(), name='process_create_form'),
    path('process_update_form/<int:pk>', ProcessUpdate.as_view(), name='process_update_form'),
    path('process_delete_confirmation/<int:pk>', ProcessDelete.as_view(), name='process_delete_confirmation'),
    path('process-modeling/', ProcessModelingView.as_view(), name="process_modeling"),
    path('ontology-suggestion', OntologySuggestionView.as_view(), name="ontology_suggestion")
]
