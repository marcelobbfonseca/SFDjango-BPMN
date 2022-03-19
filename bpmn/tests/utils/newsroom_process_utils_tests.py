import pytest, json
from bpmn.models import Ontology
from SFDjango.settings import STATIC_ROOT
from bpmn.utils.newsroom_process_utils import NewsroomProcessUtils
from bpmn.utils.process_utils import ProcessUtils

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


@pytest.fixture(scope='module')
def domain_ontology(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        domain_owl_path = STATIC_ROOT + '/bpmn/ontologies/news_publicationrdf.owl'
        ontology = Ontology.objects.create(
                name='newsroom domain', 
                prefix='http://www.semanticweb.org/oem/ontologies/2021/2/news_publication#', 
                path_name=domain_owl_path
        )
    yield ontology
    print("TEAR DOWN")
    with django_db_blocker.unblock():
        ontology.delete()

@pytest.fixture(scope='module')
def newsroom_process_utils(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        obj = NewsroomProcessUtils()
    return obj


def test_verify_task_author(domain_ontology, newsroom_process_utils):
    domain_ontology
    task = {"id":"04csnbg","description":"revisa matéria_01","x":350,"y":70}
    author = 'editor_01'
    result, _ = newsroom_process_utils.verify_task_author(author, task)
    assert result == True


def test_verify_task_wrong_author(domain_ontology, newsroom_process_utils):
    domain_ontology
    task = {"id":"04csnbg","description":"revisa matéria_01","x":350,"y":70}
    author = 'reporter_01'
    _, result = newsroom_process_utils.verify_task_author(author, task)
    assert result[0] == "editor_01"


def test_get_lane_tasks(domain_ontology, newsroom_process_utils):
    domain_ontology
    author = "reporter_01"
    tasks = newsroom_process_utils.get_lane_tasks(author)
    assert len(tasks) == 2

def test_get_tasks_by_lane():
    elements = {
        "Participant":[{"id":"0xue50s","name":""}],
        "Collaboration":[{"id":"0ete02m"},{"id":"0ete02m"}],
        "Lane":[
            {"id":"1uknwdf","author":"editor_01","x":198,"y":40},
            {"id":"1mgmwrm","author":"reporter_01","x":198,"y":165}],
        "Flow":[{"id":"1u1gs3n"},{"id":"00cgsce"},{"id":"1t4sqfy"},{"id":"03f070z"},{"id":"1u1gs3n"},{"id":"00cgsce"},{"id":"1t4sqfy"}],
        "Activity":[
            {"id":"04csnbg","description":"revisa matéria_01","x":350,"y":70},
            {"id":"09l1mrk","description":"reescreve matéria_01","x":520,"y":70},
            {"id":"0m5f9rd","description":"publica matéria_01","x":520,"y":200}
        ],
        "Event":[{"id":"1uqtwc9","description":None,"x":672,"y":222}],
        "Gateway":[],
        "StartEvent":[{"id":"1","description":None,"x":252,"y":92},{"id":"1","description":"inicio","x":257,"y":135}],
        "Process":[]
    }
    tasks_by_lane = ProcessUtils.get_tasks_by_lane(elements)
    assert len(tasks_by_lane['editor_01']) == 2
    assert len(tasks_by_lane['reporter_01']) == 1


#se escreve task errada, nao vai achar como arruma
def test_verify_tasks_by_lanes(domain_ontology, newsroom_process_utils):
    domain_ontology
    laneTasks = {
        'editor_01': [
            {'id': '04csnbg', 'description': 'revisa matéria_01', 'x': 350, 'y': 70},  
            {'id': '09l1mrk', 'description': 'reescreve matéria_01', 'x': 520, 'y': 70}
        ], 
        'reporter_01': [
            {'id': '0m5f9rd', 'description': 'publica matéria_01', 'x': 520, 'y': 200}
        ]
    }
    verified_tasks = newsroom_process_utils.verify_tasks_by_lanes(laneTasks)
    assert verified_tasks['editor_01'][0]['ok'] == True
    assert verified_tasks['editor_01'][0]['id'] == '04csnbg'

#next tests
def test_verify_process_missing_tasks(domain_ontology, newsroom_process_utils):
    laneTasks = { 
        'editor_01': [
            {'id': '04csnbg', 'description': 'revisa matéria_01', 'x': 350, 'y': 70}, 
            {'id': '09l1mrk', 'description': 'reescreve matéria_01', 'x': 520, 'y': 70}
        ], 
        'reporter_01': [
            {'id': '0m5f9rd', 'description': 'publica matéria_01', 'x': 520, 'y': 200}
        ]
    }
    missing_tasks = newsroom_process_utils.verify_process_missing_tasks(laneTasks)
    assert len(missing_tasks) == 6

def test_get_process_tasks(domain_ontology, newsroom_process_utils):
    tasks = newsroom_process_utils.get_process_tasks('produção_da_publicação')
    assert len(tasks) == 9