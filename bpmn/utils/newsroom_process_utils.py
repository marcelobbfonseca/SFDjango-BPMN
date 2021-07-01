from django.db.models import query
from bpmn.models import Ontology
import rdflib

# P O ta vazio?(task novo)
# 	Pega author Sparql com S ?P ?O.
# 	 sugestão_nova_task = resultados - existentes tasks ja existentes.
class NewsroomProcessUtils:

  def __init__(self):
    self.newsroom_ontology = Ontology.objects.get(name='newsroom domain')
    self.graph = rdflib.Graph()
    self.graph.parse(source=self.newsroom_ontology.path_name, format='xml')
    # self.newsroom_process = Ontology.objects.find()

  def get_lane_tasks(self, author):
      # return alllane tasks
      # TODO: getting non prefixed predicate! group_()
      query_string =  "SELECT ?p ?o WHERE {{ news:{} ?p ?o .}}".format(author)
      result = self.graph.query(query_string, initNs={"news": self.newsroom_ontology.prefix})
      tasks = []

      for row in result:
        if Ontology.have_prefix(row.p) and Ontology.have_prefix(row.o):
          task = "{} {}".format(Ontology.remove_prefix(row.p), Ontology.remove_prefix(row.o)) 
          tasks.append(task)

      return tasks

  def verify_task_author(self, author, task): 
    # retorna true(ASK) ou correçao(SELECT)

    predicate, obj = task['description'].split(' ')
    query_string = "ASK {{ news:{} news:{} news:{} .}}".format(author, predicate, obj)
    is_true = self.graph.query(query_string, initNs={"news": self.newsroom_ontology.prefix})
    
    if bool(is_true):
      return True, ""

    query_string = "SELECT ?author WHERE {{ ?author news:{} news:{} .}}".format(predicate, obj)
    result = self.graph.query(query_string, initNs={
                         "news": self.newsroom_ontology.prefix})
    authors = [ str(row.author) for row in result]
    return False, Ontology.remove_prefixes(authors)


  def verify_tasks_by_lanes(self, lane_tasks):
    verified_tasks = {}

    for lane in lane_tasks:
        verified_tasks[lane] = []
        for task in lane_tasks[lane]:
            if len(task['description']) == 0: # verify if empty
              author_tasks = self.get_lane_tasks(lane)
              verified_tasks[lane].append({'id':task['id'], 'ok':False, 'fix':author_tasks})
              break

            task_ok, fix = self.verify_task_author(lane, task)
            verified_tasks[lane].append({'id':task['id'], 'ok':task_ok, 'fix': [fix] })

    return verified_tasks

  # 		checagem de tarefas(triplas) que faltam pro processo
  # 		  tasks_obrigatorias = sparql com nome do processo (S P ?O)
  def verify_process_missing_tasks(self, laneTasks):
  #   process_tasks = self.get_process_tasks()
  #   existing_tasks = []
  #   for lane in laneTasks:
  #       for task in laneTasks[lane]:
  #           if task and task.strip():
  #             continue
            
  #           existing_tasks.append(task)

    return {}

  def get_process_tasks(process_name):
  #   # process_name == pool
  #   # self.newsroom_process sparql
    return {}
