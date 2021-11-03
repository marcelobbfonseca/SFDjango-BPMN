import pytest, json
from pathlib import Path
from SFDjango.settings import STATIC_ROOT
from bpmn.utils.diagram_parser_utils import DiagramParserUtils

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

@pytest.fixture(scope='module')
def diagram_xml():
    diagram = Path(STATIC_ROOT + '/bpmn/diagrams_files/simple_news_process_diagram.bpmn').read_text()
    diagram = diagram.replace('\n', '')
    return diagram

def test_parse_diagram_xml(diagram_xml):
    parser = DiagramParserUtils(diagram_xml)
    parser.parse_diagram_xml()
    import pdb;pdb.set_trace();
    assert 1 == 1

