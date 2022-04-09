from .models import *


def get_process_init(process):

    flow = process.type.flow
    appearances = {}

    for seq in flow.sequences.all():

        for item in [seq.current_event] + [seq.current_activity] + \
            list(seq.next_activity_options.all()) + list(seq.next_event_options.all()):

            appearances[item] = [0, seq]

    for seq in flow.sequences.all():

        if seq.next_activity_options:

            for act in seq.next_activity_options.all():

                appearances[act][0] += 1

        if seq.next_event_options:

            for evt in seq.next_event_options.all():

                appearances[evt][0] += 1

    keys = list(appearances.keys())
    item = keys[0]
    min = appearances[item][0]

    for key in keys:

        if appearances[key][0] < min:

            min = appearances[key] = 0
            item = key

    return appearances[item][1]

def get_possible_activities(process):

    if process.current is None:

        return [] # process first action must be an event

    else:

        seq = Sequence.objects.get(current_activity=process.current.type)

    acts = list(seq.next_activity_options.all())

    return acts

def get_possible_events(process):

    if process.status == PROCESS_POSSIBLE_STATUSES[2][0]:

        return []

    if process.current is None:

        seq = get_process_init(process)

        return [seq.current_event]

    else:

        seq = Sequence.objects.get(current_activity=process.current.type)

    evts = list(seq.next_event_options.all())

    return evts

def update_process(process, activity_index=0, event_type='', update=True):

    if event_type == POSSIBLE_EVENTS[0][0] or event_type == "Inicio": # start process

        act = Activity.objects.create(type=list(get_process_init(process).next_activity_options.all())[0])
        act.save()
        process.status = PROCESS_POSSIBLE_STATUSES[1][0]

    elif event_type == POSSIBLE_EVENTS[1][0] or event_type == "Fim": # end process

        act = None
        process.status = PROCESS_POSSIBLE_STATUSES[2][0]

    else:
        process_type = get_possible_activities(process)[activity_index]
        act = Activity.objects.create(type=process_type)
        act.save()

    if process.current:

        process.current.delete()

    process.current = act

    if update:
        
        process.save(update=False)
