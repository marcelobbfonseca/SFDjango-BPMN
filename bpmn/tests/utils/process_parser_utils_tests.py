import pytest, json
from pathlib import Path
from SFDjango.settings import STATIC_ROOT
from bpmn.utils.diagram_parser_utils import DiagramParserUtils
from bs4 import BeautifulSoup
from bpmn.models import Pool

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
    print("TEAR DOWN")
    with django_db_blocker.unblock():
        pool.delete()


def test_parse_diagram_xml(diagram_xml):
    parser = DiagramParserUtils(diagram_xml)
    parser.parse_diagram_xml()
    assert 1 == 1



def test_create_pools(diagram_xml):
    parser = DiagramParserUtils(diagram_xml)
    pools = parser.create_pools()
    assert len(pools) == 1
    assert pools[0].name == 'processo da noticia'

def test_create_lanes(pool, diagram_xml):
    parser = DiagramParserUtils(diagram_xml)
    lanes = parser.create_lanes(pool) 
    import pdb; pdb.set_trace();
    assert 1 == 1

def test_create_activities():
    pass
def test_create_sequences():
    pass
def test_create_events():
    pass
def test_create_process_type():
    pass