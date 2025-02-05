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
