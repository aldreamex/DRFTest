import pytest
from rest_framework.test import APIClient
from demo.models import Message
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_api():

    # Arrage - подготовка данных
    client = APIClient()
    Message.objects.create(user_id=1, text='test')
    User.objects.create_user('aldreamex')

    # Act - вызов методов
    response = client.get('/messages/') # отправляем запрос (имитация отправки пользователя)


    # Asert - проверка
    assert response.status_code == 200  # получаем ответ
    data = response.json()  # данные которые получаем в ответе (в виде json файла)
    # assert len(data) == 0   # в нашей БД пусто
    assert len(data) == 1   # в нашей БД есть один user - aldreamex
    assert data[0]['text'] == 'test'  # в базе данных лежит сообщение с текстом test
