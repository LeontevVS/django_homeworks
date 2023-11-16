import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient


@pytest.mark.django_db
def test_course_retrieve(client):
    assert False, "Just test example"


@pytest.mark.django_db
def test_courses_list(client):
    assert False, "Just test example"


@pytest.mark.django_db
def test_courses_list_filter_id(client):
    assert False, "Just test example"


@pytest.mark.django_db
def test_courses_list_filter_name(client):
    assert False, "Just test example"


@pytest.mark.django_db
def test_course_create():
    assert False, "Just test example"


@pytest.mark.django_db
def test_course_update(client):
    assert False, "Just test example"


@pytest.mark.django_db
def test_course_delete(client):
    assert False, "Just test example"
