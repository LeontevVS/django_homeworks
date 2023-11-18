import random

from students.models import Student, Course
from students.serializers import CourseSerializer

import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_course_retrieve(client, course_factory):
    courses = course_factory(_quantity=15)
    first_course_data = CourseSerializer(courses[0]).data
    resp = client.get(f'/api/v1/courses/{first_course_data["id"]}/')
    assert resp.status_code == 200
    resp_course_data = resp.json()
    assert resp_course_data == first_course_data


@pytest.mark.django_db
def test_courses_list(client, course_factory):
    courses = course_factory(_quantity=15)
    resp = client.get('/api/v1/courses/')
    assert resp.status_code == 200
    resp_cources = resp.json()
    for i, course in enumerate(courses):
        course_data = CourseSerializer(course).data
        assert course_data == resp_cources[i]


@pytest.mark.django_db
def test_courses_list_filter_id(client, course_factory):
    courses = course_factory(_quantity=15)
    random_course_data = CourseSerializer(random.choice(courses)).data
    resp = client.get(f'/api/v1/courses/?id={random_course_data["id"]}')
    assert resp.status_code == 200
    resp_course_data = resp.json()[0]
    assert resp_course_data == random_course_data


@pytest.mark.django_db
def test_courses_list_filter_name(client, course_factory):
    courses = course_factory(_quantity=15)
    random_course_data = CourseSerializer(random.choice(courses)).data
    resp = client.get(f'/api/v1/courses/?name={random_course_data["name"]}')
    assert resp.status_code == 200
    resp_course_data = resp.json()[0]
    assert resp_course_data == random_course_data


@pytest.mark.django_db
def test_course_create(client):
    couses_count = Course.objects.count()
    course = baker.prepare(Course)
    course_data = CourseSerializer(course).data
    resp = client.post('/api/v1/courses/', data=course_data)
    assert resp.status_code == 201
    assert Course.objects.count() == couses_count + 1
    resp_course_data = resp.json()
    id = resp_course_data['id']
    course_data['id'] = id
    db_course = Course.objects.get(id=id)
    db_course_data = CourseSerializer(db_course).data
    assert course_data == db_course_data


@pytest.mark.django_db
def test_course_update_put(client, course_factory):
    courses = course_factory(_quantity=15)
    random_course_data = CourseSerializer(random.choice(courses)).data
    new_course_data = CourseSerializer(baker.prepare(Course)).data
    id = random_course_data['id']
    new_course_data['id'] = id
    resp = client.put(f'/api/v1/courses/{id}/', data=new_course_data)
    assert resp.status_code == 200
    assert new_course_data == CourseSerializer(Course.objects.get(id=id)).data


@pytest.mark.django_db
def test_course_update_patch(client, course_factory):
    courses = course_factory(_quantity=15)
    random_course_data = CourseSerializer(random.choice(courses)).data
    course_change_data = {
        'name': 'Test course'
    }
    updated_course_data = {**random_course_data, **course_change_data}
    id = random_course_data['id']
    resp = client.patch(f'/api/v1/courses/{id}/', data=course_change_data)
    assert resp.status_code == 200
    assert updated_course_data == CourseSerializer(Course.objects.get(id=id)).data


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    courses = course_factory(_quantity=15)
    random_course_data = CourseSerializer(random.choice(courses)).data
    id = random_course_data['id']
    resp = client.delete(f'/api/v1/courses/{id}/')
    assert resp.status_code == 204
    assert len(Course.objects.all().filter(id=id)) == 0
