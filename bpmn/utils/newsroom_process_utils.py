from django.db.models import query
from bpmn.models import Ontology
import rdflib
from bpmn.utils.string_utils import snake_case

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
      # TODO: getting non prefixed predicate! group_(). filter in query
      query_string =  "SELECT ?p ?o WHERE {{ news:{} ?p ?o .}}".format(author)
      result = self.graph.query(query_string, initNs={"news": self.newsroom_ontology.prefix})
      tasks = []
      
      for row in result:
        if Ontology.have_prefix(row.p) and Ontology.have_prefix(row.o):
          if(Ontology.remove_prefix(row.p))=="type":
            continue
          task = "{} {}".format(Ontology.remove_prefix(row.p), Ontology.remove_prefix(row.o)) 
          tasks.append(task)

      return tasks

  def verify_task_author(self, author, task): 
    # retorna true(ASK) e array correçao(SELECT) se tiver 
    # import pdb; pdb.set_trace()
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
            verified_tasks[lane].append({'id':task['id'], 'ok':task_ok, 'fix': fix })

    return verified_tasks

  def verify_process_missing_tasks(self, laneTasks):
    process_tasks = self.get_process_tasks('produção_da_publicação')
    for lane in laneTasks:
        for task in laneTasks[lane]:
          for requiredTask in process_tasks:
            taskname = task['description']
            if snake_case(taskname) == requiredTask:
              process_tasks.remove(requiredTask)

    return process_tasks

  def get_process_tasks(self, process_name):
    name = snake_case(process_name)
    query_string =  "SELECT ?task WHERE {{ news:{} news:contém ?task .}}".format(name)
    result = self.graph.query(query_string, initNs={"news": self.newsroom_ontology.prefix})
    tasks = [ str(row.task) for row in result]
    return Ontology.remove_prefixes(tasks)
