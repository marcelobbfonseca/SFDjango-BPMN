import pytest, json
from rest_framework.test import APIClient
from bpmn.models import Diagram
from bpmn.views import diagram_view
from SFDjango.settings import STATIC_ROOT
from pathlib import Path
from django.contrib.auth.models import Group

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


@pytest.fixture(scope='module')
def diagram(django_db_setup, django_db_blocker):
    xml = Path(STATIC_ROOT + '/bpmn/diagrams_files/simple_news_process_diagram.bpmn').read_text()
    xml = xml.replace('\n', '')

    with django_db_blocker.unblock():
        diagram = Diagram.objects.create(
                name='my diagram', 
                svg='', 
                xml=xml
        )
    yield diagram
    with django_db_blocker.unblock():
        diagram.delete()

@pytest.fixture(scope='module')
def client():
    yield APIClient()

@pytest.fixture(scope='module')
def view():
    yield diagram_view.as_view()

@pytest.fixture(scope='module')
def diagram_params():
    xml = Path(STATIC_ROOT + '/bpmn/diagrams_files/simple_news_process_diagram.bpmn').read_text()
    xml = xml.replace('\n', '')
    return {
        'name': 'my diagram',
        'xml': xml,
        'svg': """
            <?xml version=\"1.0\" encoding=\"utf-8\"?>\n
            <!-- created with bpmn-js / http://bpmn.io -->\n
            <!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n
            <svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" 
            width=\"612\" height=\"262\" viewBox=\"264 34 612 262\" version=\"1.1\"><defs>
            <marker id=\"sequenceflow-end-white-black-as9qjjlgoouhnrys9z2r3f66m\" viewBox=\"0 0 20 20\" refX=\"11\" 
            refY=\"10\" markerWidth=\"10\" markerHeight=\"10\" orient=\"auto\">
            <path d=\"M 1 5 L 11 10 L 1 15 Z\" style=\"fill: black; stroke-width: 1px; stroke-linecap: round;
            stroke-dasharray: 10000px, 1px; stroke: black;\"/></marker></defs><g class=\"djs-group\">
            <g class=\"djs-element djs-shape\" data-element-id=\"Participant_119qlvo\"
            transform=\"matrix(1, 0, 0, 1, 270, 40)\" style=\"display: block;\"><g class=\"djs-visual\">
            <rect x=\"0\" y=\"0\" width=\"600\" height=\"250\" rx=\"0\" ry=\"0\" style=\"stroke: black; 
            stroke-width: 2px; fill: white; fill-opacity: 0.95;\"/>
            <polyline points=\"30,0 30,250 \" style=\"fill: none; stroke: black; stroke-width: 2px;\"/>
            <text style=\"font-family: Arial, sans-serif; font-size: 12px; font-weight: normal; fill: black;\" 
            lineHeight=\"1.2\" class=\"djs-label\" transform=\"matrix(-1.83697e-16, -1, 1, -1.83697e-16, 0, 250)\">
            <tspan x=\"125\" y=\"18.6\"/></text></g>
            <rect x=\"-6\" y=\"-6\" width=\"612\" height=\"262\" style=\"fill: none;\" class=\"djs-outline\"/>
            <rect style=\"fill: none; stroke-opacity: 0; stroke: white; stroke-width: 15px;\" 
            class=\"djs-hit djs-hit-click-stroke\" x=\"0\" y=\"0\" width=\"600\" height=\"250\"/>
            <rect style=\"fill: none; stroke-opacity: 0; stroke: white; stroke-width: 15px;\"
            class=\"djs-hit djs-hit-all\" x=\"0\" y=\"0\" width=\"30\" height=\"250\"/></g><g class=\"djs-children\">
            <g class=\"djs-group\"><g class=\"djs-element djs-connection\" data-element-id=\"Flow_0pwalac\"
            style=\"display: block;\"><g class=\"djs-visual\">
            <path d=\"m  358,100L420,100 \" style=\"fill: none; stroke-width: 2px;
            stroke: black; stroke-linejoin: round; 
            marker-end: url('#sequenceflow-end-white-black-as9qjjlgoouhnrys9z2r3f66m');\"/></g>
            <polyline points=\"358,100 420,100 \" style=\"fill: none; stroke-opacity: 0; 
            stroke: white; stroke-width: 15px;\" class=\"djs-hit djs-hit-stroke\"/>
            <rect x=\"352\" y=\"94\" width=\"74\" height=\"12\" style=\"fill: none;\" class=\"djs-outline\"/></g></g>
            <g class=\"djs-group\"><g class=\"djs-element djs-connection\" data-element-id=\"Flow_1en9gxg\"
            style=\"display: block;\"><g class=\"djs-visual\">
            <path d=\"m  520,100L590,100 \" style=\"fill: none; stroke-width: 2px; stroke: black; stroke-linejoin: round;
            marker-end: url('#sequenceflow-end-white-black-as9qjjlgoouhnrys9z2r3f66m');\"/></g>
            <polyline points=\"520,100 590,100 \" style=\"fill: none; stroke-opacity: 0; stroke: white;
            stroke-width: 15px;\" class=\"djs-hit djs-hit-stroke\"/>
            <rect x=\"514\" y=\"94\" width=\"82\" height=\"12\" style=\"fill: none;\" class=\"djs-outline\"/></g></g>
            <g class=\"djs-group\"><g class=\"djs-element djs-connection\" data-element-id=\"Flow_01q0xkq\"
            style=\"display: block;\"><g class=\"djs-visual\">
            <path d=\"m  690,100L762,100 \" style=\"fill: none; stroke-width: 2px; stroke: black; stroke-linejoin: round;
            marker-end: url('#sequenceflow-end-white-black-as9qjjlgoouhnrys9z2r3f66m');\"/></g>
            <polyline points=\"690,100 762,100 \" style=\"fill: none; stroke-opacity: 0; stroke: white; 
            stroke-width: 15px;\" class=\"djs-hit djs-hit-stroke\"/><rect x=\"684\" y=\"94\" width=\"84\"
             height=\"12\" style=\"fill: none;\" class=\"djs-outline\"/></g></g><g class=\"djs-group\">
            <g class=\"djs-element djs-shape\" data-element-id=\"StartEvent_1\" transform=\"matrix(1, 0, 0, 1, 322, 82)\"
            style=\"display: block;\"><g class=\"djs-visual\"><circle cx=\"18\" cy=\"18\" r=\"18\" style=\"stroke: black;
            stroke-width: 2px; fill: white; fill-opacity: 0.95;\"/></g><rect style=\"fill: none; stroke-opacity: 0;
            stroke: white; stroke-width: 15px;\" class=\"djs-hit djs-hit-all\" x=\"0\" y=\"0\" width=\"36\"
            height=\"36\"/><rect x=\"-6\" y=\"-6\" width=\"48\" height=\"48\" style=\"fill: none;\"
            class=\"djs-outline\"/></g></g><g class=\"djs-group\"><g class=\"djs-element djs-shape\"
            data-element-id=\"Activity_0a82qi1\" transform=\"matrix(1, 0, 0, 1, 420, 60)\" style=\"display: block;\">
            <g class=\"djs-visual\"><rect x=\"0\" y=\"0\" width=\"100\" height=\"80\" rx=\"10\" ry=\"10\" 
            style=\"stroke: black; stroke-width: 2px; fill: white; fill-opacity: 0.95;\"/><text style=\"font-family: Arial, 
            sans-serif; font-size: 12px; font-weight: normal; fill: black;\" lineHeight=\"1.2\" class=\"djs-label\">
            <tspan x=\"50\" y=\"43.599999999999994\"/></text></g>
            <rect style=\"fill: none; stroke-opacity: 0; stroke: white; stroke-width: 15px;\" class=\"djs-hit djs-hit-all\" 
            x=\"0\" y=\"0\" width=\"100\" height=\"80\"/><rect x=\"-6\" y=\"-6\" width=\"112\" height=\"92\" 
            style=\"fill: none;\" class=\"djs-outline\"/></g></g><g class=\"djs-group\">
            <g class=\"djs-element djs-shape\" data-element-id=\"Activity_04bfxby\" transform=\"matrix(1, 0, 0, 1, 590, 60)\" 
            style=\"display: block;\"><g class=\"djs-visual\"><rect x=\"0\" y=\"0\" width=\"100\" 
            height=\"80\" rx=\"10\" ry=\"10\" style=\"stroke: black; stroke-width: 2px; fill: white; fill-opacity: 0.95;\"/>
            <text style=\"font-family: Arial, sans-serif; font-size: 12px; font-weight: normal; fill: black;\" lineHeight=\"1.2\" 
            class=\"djs-label\"><tspan x=\"50\" y=\"43.599999999999994\"/></text></g><rect style=\"fill: none; 
            stroke-opacity: 0; stroke: white; stroke-width: 15px;\" class=\"djs-hit djs-hit-all\" x=\"0\" y=\"0\" 
            width=\"100\" height=\"80\"/><rect x=\"-6\" y=\"-6\" width=\"112\" height=\"92\" style=\"fill: none;\" 
            class=\"djs-outline\"/></g></g><g class=\"djs-group\">
            <g class=\"djs-element djs-shape\" data-element-id=\"Event_1hsi1pj\" transform=\"matrix(1, 0, 0, 1, 762, 82)\" 
            style=\"display: block;\"><g class=\"djs-visual\"><circle cx=\"18\" cy=\"18\" r=\"18\" style=\"stroke: black; 
            stroke-width: 4px; fill: white; fill-opacity: 0.95;\"/></g>
            <rect style=\"fill: none; stroke-opacity: 0; stroke: white; stroke-width: 15px;\" class=\"djs-hit djs-hit-all\" x=\"0\" 
            y=\"0\" width=\"36\" height=\"36\"/><rect x=\"-6\" y=\"-6\" width=\"48\" height=\"48\" style=\"fill: none;\" 
            class=\"djs-outline\"/></g></g></g></g></svg>"
        """
    }

@pytest.fixture(scope='module')
def groups(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        group1 = Group.objects.create(name='Editor')
        group2 = Group.objects.create(name='Reporter')
    yield (group1, group2)
    with django_db_blocker.unblock():
        group1.delete()
        group2.delete()


def test_list(client, diagram):
    diagram
    response = client.get('/api/v1/diagrams/')
    content_body = json.loads(response.content.decode('utf-8'))
    
    assert response.status_code == 200
    assert content_body[0]['name'] == 'my diagram'

def test_create(client, diagram_params, groups):
    groups
    response = client.post('/api/v1/diagrams/',diagram_params, format='json')
    assert response.status_code == 200