import pytest, json
from pathlib import Path
from SFDjango.settings import STATIC_ROOT
from bpmn.utils.diagram_parser_utils import DiagramParserUtils
from bs4 import BeautifulSoup
from bpmn.models import Pool, Lane, Event, Flow, ProcessType
from django.contrib.auth.models import Group

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

@pytest.fixture(scope='module')
def diagram_xml():
    diagram = Path(STATIC_ROOT + '/bpmn/diagrams_files/simple_news_process_diagram.bpmn').read_text()
    diagram = diagram.replace('\n', '')
    return diagram

@pytest.fixture(scope='module')
def bs_content(diagram_xml):
    content = []
    content = "".join(diagram_xml)
    return BeautifulSoup(content, 'lxml')

@pytest.fixture(scope='module')
def pool(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        pool = Pool.objects.create(name='processo da noticia')
    yield pool
    with django_db_blocker.unblock():
        pool.delete()

@pytest.fixture(scope='module')
def groups(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        group1 = Group.objects.create(name='Editor')
        group2 = Group.objects.create(name='Reporter')
    yield (group1, group2)
    with django_db_blocker.unblock():
        group1.delete()
        group2.delete()

@pytest.fixture(scope='module')
def reporter_lane(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        pool = Pool.objects.create(name='processo da noticia')
        group = Group.objects.create(name='Reporter')
        lane = Lane.objects.create(name='reporter_01', pool=pool, responsable=group)
    yield lane 
    with django_db_blocker.unblock():
        lane.delete()

@pytest.fixture(scope='module')
def editor_lane(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        pool = Pool.objects.create(name='processo da noticia')
        group = Group.objects.create(name='Editor')
        lane = Lane.objects.create(name='editor_01', pool=pool, responsable=group)
    yield lane 
    with django_db_blocker.unblock():
        lane.delete()


@pytest.fixture(scope='module')
def create_events(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        start_event = Event.objects.create(name='Inicio', diagram_id='StartEvent_0p87cuw')
        end_event = Event.objects.create(name='Fim', diagram_id='Event_0b0tg3w')
    yield start_event, end_event
    with django_db_blocker.unblock():
        start_event.delete()
        end_event.delete()
    
@pytest.fixture(scope='module')
def create_flow(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        flow = Flow.objects.create()
    yield flow
    with django_db_blocker.unblock():
        flow.delete()

# def test_parse_diagram_xml_and_create_process(diagram_xml, groups):
#     groups
#     parser = DiagramParserUtils(diagram_xml)
#     process_type = parser.parse_diagram_xml_and_create_process()
#     assert isinstance(process_type, ProcessType)

def test_create_pools(diagram_xml):
    parser = DiagramParserUtils(diagram_xml)
    pools = parser.create_pools()
    assert len(pools) == 1
    assert pools[0].name == 'processo da noticia'

def test_create_lanes(pool, diagram_xml, groups):
    groups
    parser = DiagramParserUtils(diagram_xml)
    lanes = parser.create_lanes(pool) #
    assert len(lanes) == 2

# def test_create_activities(diagram_xml, reporter_lane):
#     parser = DiagramParserUtils(diagram_xml)
#     activities, atypes = parser.create_activities(reporter_lane)
#     assert len(activities) == len(atypes)
#     assert len(atypes) == 2

def test_create_events(diagram_xml):
    parser = DiagramParserUtils(diagram_xml)
    events = parser.create_events()
    assert len(events) == 2

def test_create_sequences(diagram_xml, create_events, reporter_lane, editor_lane):
    create_events
    # need activities created
    parser = DiagramParserUtils(diagram_xml)
    parser.create_activities(reporter_lane)
    parser.create_activities(editor_lane)

    sequences, _ = parser.create_sequences() #
    assert len(sequences) == 9

def test_create_process_type(diagram_xml, create_flow):
    flow = create_flow
    parser = DiagramParserUtils(diagram_xml)
    process_type = parser.create_process_type(flow)
    assert process_type.id != None
    assert isinstance(process_type, ProcessType)
