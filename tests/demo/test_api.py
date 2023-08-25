import pytest
from rest_framework.test import APIClient
from demo.models import Message
from django.contrib.auth.models import User
from model_bakery import baker

# создаем клиента для всех тестов
@pytest.fixture
def client():
    return APIClient()


# создаем пользователя для всех тестов
@pytest.fixture
def user():
    return User.objects.create_user('aldreamex')

# создаем сообщения для всех тестов
@pytest.fixture
def message_factory():
    def factory(*args, **kwargs):
        return baker.make(Message, *args, **kwargs)

    return factory

@pytest.mark.django_db
def test_get_messages(client, user, message_factory):

    # Arrage - подготовка данных
    # client = APIClient()
    # Message.objects.create(user_id=user.id, text='test')
    messages = message_factory(_quantity=10)    # создаем 10 сообщений
    # User.objects.create_user('aldreamex')

    # Act - вызов методов
    response = client.get('/messages/') # отправляем запрос (имитация отправки пользователя)


    # Asert - проверка
    assert response.status_code == 200  # получаем ответ
    data = response.json()  # данные которые получаем в ответе (в виде json файла)
    # assert len(data) == 0   # в нашей БД пусто
    assert len(data) == len(messages)   # сколько записей в бд
    # assert data[0]['text'] == 'test'  # в базе данных лежит сообщение с текстом test
    for i, m in enumerate(data):    # данные от сервера равны данным в БД
        assert m['text'] == messages[i].text

@pytest.mark.django_db
def test_create_message(client, user):
    count = Message.objects.count() # количество сообщений в БД

    # User.objects.create_user('aldreamex1')
    response = client.post('/messages/', data={'user': user.id, 'text': 'text message'})

    assert response.status_code == 201  # post запрос отправлен

    assert Message.objects.count() == count + 1 # количество сообщений увеличилось на 1 (после запроса)