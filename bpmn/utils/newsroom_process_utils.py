from bpmn.models import Ontology
import rdflib


class NewsroomProcessUtils:

  def __init__(self):
    self.newsroom_ontology = Ontology.objects.get(name='newsroom domain')
    # self.newsroom_process = Ontology.objects.find()

  def get_lane_tasks(self, author):
      # return alllane tasks
      pass

  # P O ta vazio?(task novo)
  # 	Pega author Sparql com S ?P ?O.
  # 	 sugestão_nova_task = resultados - existentes tasks ja existentes.

  def verify_task_author(self, author, task):
    # retorna true(ASK) ou correçao(SELECT)
    # verify task empty here
    predicate, obj = task.split(' ')
    query_string = "SELECT * WHERE { ?p news:%s ?s .}" % predicate  # ask
    graph = rdflib.Graph()
    graph.parse(source=self.newsroom_ontology.path_name, format='xml')
    result = graph.query(query_string, initNs={
                         "news": self.newsroom_ontology.prefix})
    return result

  # @return dict {
  # 'task_id': {ok: True, fix: ''},
  # 'task_id': {ok: False,fix:'Editor apura pauta'}
  # }
  def verify_tasks_by_lanes(self, laneTasks):
    result = {'suggest': {'lane': []}, 'tasks': []}
    for lane in laneTasks:
        for task in laneTasks[lane]:
            if task and task.strip():
              lane_tasks= self.get_lane_tasks(lane)
              result['suggest']['lane']= lane_tasks
              continue

            self.verify_task_author(lane, task)

    return result

  # 		checagem de tarefas(triplas) que faltam pro processo
  # 			tasks_obrigatorias = sparql com nome do processo (S P ?O)
  def verify_process_missing_tasks(self, laneTasks):
    process_tasks = self.get_process_tasks()
    existing_tasks = []
    for lane in laneTasks:
        for task in laneTasks[lane]:
            if task and task.strip():
              continue
            
            existing_tasks.append(task)

    return {}

  def get_process_tasks(process_name):
    # process_name == pool
    # self.newsroom_process sparql
    return {}
