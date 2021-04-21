from django.contrib import admin
from django.shortcuts import render, redirect
from django.utils.html import format_html
from django.conf.urls import re_path
from django.http import HttpResponseRedirect
from itertools import chain
from .manager import update_process, get_possible_activities, get_possible_events
from .models import ProcessType, Process, Pool, Lane, ActivityType, Activity, Flow, Sequence, Event


for class_ in [ProcessType, \
    Pool, \
    Lane, \
    ActivityType, Activity, \
    Flow, Sequence,
    Event]:
    admin.site.register(class_)

@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):

    readonly_fields = ('status',
                       'current',
                      )
    list_display = ('id',
                    '__str__',
                    'status',
                    'current_activity',
                    'possible_actions',
                   )

    def get_queryset(self, request):

        qs = super(ProcessAdmin, self).get_queryset(request)
        qs1 = None
        qss = []

        if request.user.is_superuser:

            return qs

        for group in request.user.groups.all():

            print(group)
            qss.append(qs.filter(current__type__lane__responsable=group) | qs.filter(current=None))

        qs1 = qss[0]

        for qs in qss[1:]:

            qs1 = qs1 | qs

        return qs1

    def get_urls(self):

        urls = super().get_urls()
        my_urls = [
            re_path('update_process_/', self.update_process_),
        ]

        return my_urls + urls

    def update_process_(self, request):

        process_id, param1 = request.get_full_path().split('/')[-1].split('-')
        process = self.model.objects.get(pk=int(process_id))

        if param1.isdigit():

            param1 = int(param1)
            update_process(process, activity_index=param1)

        else:

            update_process(process, event_type=param1.replace('%20', ' '))

        return redirect("../../../../process_list/")

    def current_activity(self, obj):

        if obj.current:

            return format_html('<a href="../activity/{}">{}</a>',
                obj.current.id, obj.current.type.name)

        else:

            return ''

    def possible_actions(self, obj):

        html = ''

        for index, act in enumerate(get_possible_activities(obj)):

            html += '<a class="button" href="./update_process_/{}-{}">{}</a> &nbsp'.format(obj.id, index, str(act))
        
        for index, evt in enumerate(get_possible_events(obj)):

            html += '<a class="button" style="background-color:#ff86c5;" href="./update_process_/{}-{}">{}</a> &nbsp'.format(obj.id, evt.name, str(evt))

        return format_html(html)
