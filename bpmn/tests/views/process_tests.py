
import pytest, json
from bpmn.models import Ontology
from SFDjango.settings import STATIC_ROOT

@pytest.mark.django_db
def test_hello_world(client):
    assert 1 == 1




@pytest.mark.django_db
def test_ontology_suggestion(client):
    data = {"hello": "hi"}
    headers = {'Content-Type':'application/json'}

    domain_owl_path = STATIC_ROOT + '/bpmn/ontologies/news_publicationrdf.owl'
    Ontology.objects.create(
        name='newsroom domain', 
        prefix='http://www.semanticweb.org/oem/ontologies/2021/2/news_publication#', 
        path_name=domain_owl_path
    )

    response = client.post(path='/ontology-suggestion', data=json.dumps(data), content_type='json')
    assert response.status_code == 200
