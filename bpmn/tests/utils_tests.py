import pytest, json
from bpmn.models import Ontology
from SFDjango.settings import STATIC_ROOT
from bpmn.utils.newsroom_process_utils import NewsroomProcessUtils

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


def test_hello_world(client):
    assert 1 == 1

def test_verify_task_author(domain_ontology, newsroom_process_utils):
    domain_ontology
    task = 'revisa matéria_01'
    author = 'editor_01'
    print("hi")
    result = newsroom_process_utils.verify_task_author(author, task)
    assert result == True


def test_verify_task_wrong_author(domain_ontology, newsroom_process_utils):
    # test editor revisa materia
    domain_ontology
    task = 'revisa matéria_01'
    author = 'reporter_01'
    result = newsroom_process_utils.verify_task_author(author, task)
    assert result[0] == "editor_01"


def test_get_lane_tasks(domain_ontology):
    print("hello")
    assert 2 == 2