
import pytest, json


@pytest.mark.django_db
def test_hello_world(client):
    assert 1 == 1


def test_ontology_suggestion(client):
    data = {"hello": "hi"}
    headers = {'Content-Type':'application/json'}

    response = client.post(path='/ontology-suggestion', data=json.dumps(data), content_type='json')
    assert response.status_code == 200
