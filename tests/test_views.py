import pytest
import json
from django.test import RequestFactory
from home.views import search, view_trendings_results

@pytest.mark.django_db
def test_search_view_with_query1():
    factory = RequestFactory()
    request = factory.get('/search/', {'q': 'Oppenheimer', 'type': 'movie'})
    response = search(request)
    assert response.status_code == 200
    assert 'Oppenheimer' in response.content.decode()

@pytest.mark.django_db
def test_search_view_with_query2():
    factory = RequestFactory()
    request = factory.get('/search/', {'q': 'Castaway', 'type': 'tv'})
    response = search(request)
    assert response.status_code == 200
    assert 'Castaway' in response.content.decode()

@pytest.mark.django_db
def test_search_view_without_query():
    factory = RequestFactory()
    request = factory.get('/search/')
    response = search(request)
    assert response.status_code == 200
    assert 'Please enter a search query' in response.content.decode()

@pytest.mark.django_db
def test_view_trendings_results1():
    factory = RequestFactory()
    request = factory.get('/api/trendings/', {'media_type': 'movie', 'time_window': 'week'})
    response = view_trendings_results(request)

    assert response.status_code == 200
    json_data = json.loads(response.content.decode('utf-8'))
    assert 'results' in json_data

@pytest.mark.django_db
def test_view_trendings_results2():
    factory = RequestFactory()
    request = factory.get('/api/trendings/', {'media_type': 'tv', 'time_window': 'week'})
    response = view_trendings_results(request)

    assert response.status_code == 200
    json_data = json.loads(response.content.decode('utf-8'))
    assert 'results' in json_data