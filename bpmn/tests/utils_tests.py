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
    task = 'revisa matéria_01'
    author = 'editor_01'
    print("hi")
    result, _ = newsroom_process_utils.verify_task_author(author, task)
    assert result == True


def test_verify_task_wrong_author(domain_ontology, newsroom_process_utils):
    domain_ontology
    task = 'revisa matéria_01'
    author = 'reporter_01'
    _, result = newsroom_process_utils.verify_task_author(author, task)
    assert result[0] == "editor_01"


def test_get_lane_tasks(domain_ontology, newsroom_process_utils):
    domain_ontology
    author = "reporter_01"
    tasks = newsroom_process_utils.get_lane_tasks(author)
    assert len(tasks) == 4

def test_get_tasks_by_lane():
    elements = {
        "Participant":[{"id":"0xue50s","name":""}],
        "Collaboration":[{"id":"0ete02m"},{"id":"0ete02m"}],
        "Lane":[
            {"id":"1uknwdf","author":"Editor","x":198,"y":40},
            {"id":"1mgmwrm","author":"Reporter","x":198,"y":165}],
        "Flow":[{"id":"1u1gs3n"},{"id":"00cgsce"},{"id":"1t4sqfy"},{"id":"03f070z"},{"id":"1u1gs3n"},{"id":"00cgsce"},{"id":"1t4sqfy"}],
        "Activity":[
            {"id":"04csnbg","description":"revisar matéria","x":350,"y":70},
            {"id":"09l1mrk","description":"reescreve matéria","x":520,"y":70},
            {"id":"0m5f9rd","description":"publicar matéria","x":520,"y":200}
        ],
        "Event":[{"id":"1uqtwc9","description":None,"x":672,"y":222}],
        "Gateway":[],
        "StartEvent":[{"id":"1","description":None,"x":252,"y":92},{"id":"1","description":"inicio","x":257,"y":135}],
        "Process":[]
    }
    tasks_by_lane = ProcessUtils.get_tasks_by_lane(elements)
    assert len(tasks_by_lane['Editor']) == 2
    assert len(tasks_by_lane['Reporter']) == 1


def test_verify_tasks_by_lanes(domain_ontology, newsroom_process_utils):
    domain_ontology
    laneTasks = {
        'Editor': [
            {'id': '04csnbg', 'description': 'revisar matéria', 'x': 350, 'y': 70}, 
            {'id': '09l1mrk', 'description': 'reescreve matéria', 'x': 520, 'y': 70}
        ], 
        'Reporter': [
            {'id': '0m5f9rd', 'description': 'publicar matéria', 'x': 520, 'y': 200}
        ]
    }
    verified_tasks = newsroom_process_utils.verify_tasks_by_lanes(laneTasks)

    assert verified_tasks['Editor'][0]['ok'] == False
    assert verified_tasks['Editor'][0]['id'] == '04csnbg'

def test_verify_process_missing_tasks():
    assert 1 == 1