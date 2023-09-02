import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student
import json

# def test_example():
#     assert False, "Just test example"

# фикстура для ари клиентов
@pytest.fixture
def api_client():
    return APIClient()

# фикстура для фабрики курсов
@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

# фикстура для фабрики студентов
@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


# Тест 1. проверка получения первого курса
@pytest.mark.django_db
def test_one_courses(api_client, course_factory):
    courses = course_factory(_quantity=1)[0]
    response = api_client.get(f"/api/v1/courses/{courses.id}/")
    assert response.status_code == 200
    assert response.data['id'] == courses.id
    assert response.data['name'] == courses.name


# Тест 2. проверка получения списка курсов
@pytest.mark.django_db
def test_list_course(api_client, course_factory):
    count_course = 5
    courses = course_factory(_quantity=count_course)
    response = api_client.get(f"/api/v1/courses/")
    assert response.status_code == 200
    assert len(response.data) == count_course
    for i, m in enumerate(courses):
        assert response.data[i]['id'] == m.id
        assert response.data[i]['name'] == m.name


# Тест 3. проверка фильтрации списка курсов по id
# Тест 4. проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_course_id(api_client, course_factory):
    courses = course_factory(_quantity=5)
    response = api_client.get(f"/api/v1/courses/")
    course_filter = courses[1]
    assert response.status_code == 200
    assert len(response.data) == 5
    filtered_courses = [course for course in response.data if course['id'] == course_filter.id]
    assert len(filtered_courses) == 1
    assert response.data[1]['id'] == course_filter.id
    assert response.data[1]['name'] == course_filter.name


# Тест 5. тест успешного создания курса
# здесь фабрика не нужна, готовим JSON-данные и создаём курс;
@pytest.mark.django_db
def test_new_course(api_client):
    course_new = {
        "name": "New Course",
    }
    response = api_client.post(f"/api/v1/courses/", data=json.dumps(course_new), content_type="application/json")
    assert response.status_code == 201
    create_json = response.json()
    assert 'id' in create_json
    assert create_json['name'] == course_new['name']


# Тест 6. тест успешного обновления курса:
# сначала через фабрику создаём, потом обновляем JSON-данными
@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    courses = course_factory(_quantity=1)
    course_update = {
        "name": "New Course Name",
    }
    response = api_client.put(f"/api/v1/courses/{courses[0].id}/", data=json.dumps(course_update), content_type="application/json")
    assert response.status_code == 200
    update_json = response.json()
    assert 'id' in update_json
    assert update_json['name'] == course_update['name']

# Тест 7. тест успешного удаления курса.
@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    courses = course_factory(_quantity=150)
    course_id = courses[10].id
    response = api_client.delete(f"/api/v1/courses/{course_id}/")
    assert response.status_code == 204
    deleted_course = Course.objects.filter(id=course_id).first()
    assert deleted_course is None