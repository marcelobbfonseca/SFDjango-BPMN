

class ProcessUtils:


    # return dict list with tasks description per Lane
    # {'editor': ['aprova materia', 'publica materia'] }
    @staticmethod #pytest this!
    def get_tasks_by_lane(elements):
        if 'Activity' not in elements and len(elements['Activity']) == 0:
            return {}
        if len(elements['Lane']) ==0:
            return {}

        tasks_by_lanes = init_lanes(elements['Lane'])

        distance, author = 9999, ''
        for activity in elements['Activity']:
            for lane in elements['Lane']:
                if(abs(activity['y'] - lane['y'])) < distance:
                    distance, author = abs(activity['y'] - lane['y']), lane['author']
            
            tasks_by_lanes[author].append(activity)
            distance = 9999

        return tasks_by_lanes


def init_lanes(lanes):
    lanes_dict = {}
    for lane in lanes:
        author = lane['author']
        lanes_dict[author] = []
    
    return lanes_dict