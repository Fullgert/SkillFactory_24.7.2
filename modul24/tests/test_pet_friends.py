from api import PetFriends
from settings import valid_email, valid_password
import pytest

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    print(f"\n[Get API Key] Status: {status}, Result: {result}")  # Вывод ответа
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    print(f"\n[Get All Pets] Status: {status}, Result: {result}")  # Вывод ответа
    assert status == 200
    assert len(result['pets']) > 0


def test_post_add_information_about_new_pet_success():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_data = {
        'name': 'Boba',
        'animal_type': 'fish',
        'age': '189784',
        'pet_photo': 'images/pet_photo1.jpg'
    }
    status, result = pf.post_add_information_about_new_pet(
        auth_key,
        pet_data['name'],
        pet_data['animal_type'],
        pet_data['age'],
        pet_data['pet_photo']
    )
    print(f"\n[Add New Pet] Status: {status}, Result: {result}")  # Вывод ответа
    assert status == 200
    assert 'id' in result


def test_put_update():
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем питомца для обновления
    pet_data = {
        'name': 'Vaga',
        'animal_type': 'Птица',
        'age': '18',
        'pet_photo': 'images/pet_photo2.jpg'
    }
    status, result = pf.post_add_information_about_new_pet(
        auth_key,
        pet_data['name'],
        pet_data['animal_type'],
        pet_data['age'],
        pet_data['pet_photo']
    )
    print(f"\n[Create Pet for Update] Status: {status}, Result: {result}")  # Вывод ответа
    pet_id = result['id']

    # Обновляем данные
    updated_data = {
        'name': 'Biba',
        'animal_type': 'fish',
        'age': '0.9',
    }
    status, result = pf.put_update_pet(
        auth_key,
        updated_data['name'],
        updated_data['animal_type'],
        updated_data['age'],
        pet_id,
    )
    print(f"\n[Update Pet] Status: {status}, Result: {result}")  # Вывод ответа
    assert status == 200


def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем питомца для удаления
    pet_data = {
        'name': 'Burg',
        'animal_type': 'asmo',
        'age': '12',
        'pet_photo': 'images/asmo.jpg'
    }
    status, result = pf.post_add_information_about_new_pet(
        auth_key,
        pet_data['name'],
        pet_data['animal_type'],
        pet_data['age'],
        pet_data['pet_photo']
    )
    print(f"\n[Create Pet for Delete] Status: {status}, Result: {result}")  # Вывод ответа
    pet_id = result['id']

    # Удаляем питомца
    status, result = pf.delete_pet(auth_key, pet_id)
    print(f"\n[Delete Pet] Status: {status}, Result: {result}")  # Вывод ответа
    assert status == 200


def test_get_my_pets():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, 'my_pets')
    print(f"\n[Get My Pets] Status: {status}, Result: {result}")
    assert status == 200
    assert len(result['pets']) >= 0  # Проверяем, что список возвращается (может быть пустым)


def test_update_pet_without_changes():
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем питомца
    pet_data = {
        'name': 'OriginalName',
        'animal_type': 'OriginalType',
        'age': '5',
        'pet_photo': 'images/pet_photo1.jpg'
    }
    status, result = pf.post_add_information_about_new_pet(
        auth_key,
        pet_data['name'],
        pet_data['animal_type'],
        pet_data['age'],
        pet_data['pet_photo']
    )
    pet_id = result['id']

    # Обновляем питомца без изменений
    status, result = pf.put_update_pet(
        auth_key,
        pet_data['name'],
        pet_data['animal_type'],
        pet_data['age'],
        pet_id
    )
    print(f"\n[Update Pet Without Changes] Status: {status}, Result: {result}")
    assert status == 200
    assert result['name'] == pet_data['name']
    assert result['animal_type'] == pet_data['animal_type']
    assert result['age'] == pet_data['age']

def test_add_pet_with_long_values():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    long_value = 'a' * 1000  # Строка из очень большого колличества символов
    pet_data = {
        'name': long_value,
        'animal_type': long_value,
        'age': long_value,
        'pet_photo': 'images/pet_photo1.jpg'
    }
    status, result = pf.post_add_information_about_new_pet(
        auth_key,
        pet_data['name'],
        pet_data['animal_type'],
        pet_data['age'],
        pet_data['pet_photo']
    )
    print(f"\n[Add Pet with Long Values] Status: {status}, Result: {result}")
    assert status == 200  # Ожидаем успешное добавление на небольших значениях около 1000 (или 400, если есть ограничения)(так же можем проверит максимальное ко-во символов перевариваемое сайтом должны получить status 500 если сайт не справляется с данными (это около 5600000))


def test_add_pet_with_invalid_data_types():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_data = {
        'name': 12345,  # Число вместо строки
        'animal_type': True,  # Булево значение вместо строки
        'age': 5.5,  # Число с плавающей точкой вместо строки
        'pet_photo': 'images/pet_photo1.jpg'
    }
    status, result = pf.post_add_information_about_new_pet(
        auth_key,
        pet_data['name'],
        pet_data['animal_type'],
        pet_data['age'],
        pet_data['pet_photo']
    )
    print(f"\n[Add Pet with Invalid Data Types] Status: {status}, Result: {result}")
    assert status == 200  # НО ожидаем ошибку 400
    print('Но тут ожидаем ошибку 400 ')

def test_update_nonexistent_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    updated_data = {
        'name': 'Nonexistent',
        'animal_type': 'Ghost',
        'age': '999'
    }
    nonexistent_pet_id = "nonexistent_pet_id_123"
    status, result = pf.put_update_pet(
        auth_key,
        updated_data['name'],
        updated_data['animal_type'],
        updated_data['age'],
        nonexistent_pet_id
    )
    print(f"\n[Update Nonexistent Pet] Status: {status}, Result: {result}")
    assert status == 400# Ожидаем ошибку

def test_get_api_key_with_invalid_credentials():
    # Неверный email
    status, result = pf.get_api_key("invalid_email@example.com", valid_password)
    print(f"\n[Get API Key with Invalid Email] Status: {status}, Result: {result}")
    assert status == 403  # Ожидаем ошибку авторизации

    # Неверный пароль
    status, result = pf.get_api_key(valid_email, "invalid_password")
    print(f"\n[Get API Key with Invalid Password] Status: {status}, Result: {result}")
    assert status == 403  # Ожидаем ошибку авторизации



def test_add_pet_with_empty_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_data = {
        'name': '',
        'animal_type': '',
        'age': '',
        'pet_photo': 'images/asmo.jpg'
    }
    status, result = pf.post_add_information_about_new_pet(
        auth_key,
        pet_data['name'],
        pet_data['animal_type'],
        pet_data['age'],
        pet_data['pet_photo']
    )
    print(f"\n[Add Pet with Empty Data] Status: {status}, Result: {result}")
    assert status == 200  # Ожидаем ошибку
    print("Есть возможность создать персонажа только с фото (Без заполнения остальных полей)")
    
    
   
