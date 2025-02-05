import requests


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password

        }
        res = requests.get(f'{self.base_url}api/key', headers=headers)

        status = res.status_code
        result = res.json()
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(f'{self.base_url}api/pets', headers=headers, params=filter)

        status = res.status_code
        result = res.json()
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_information_about_new_pet(self, auth_key, name, animal_type, age, pet_photo, res=None):

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}
        files = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(f'{self.base_url}api/pets', headers=headers, data=data, files=files)
        status = res.status_code
        result = res.json()
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def put_update_pet(self, auth_key, name, animal_type, age, pet_id):
        path = {'pet_id': pet_id}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}
        # Используем PUT для обновления данных
        res = requests.put(f'{self.base_url}api/pets/{pet_id}', headers=headers, data=data)

        status = res.status_code

        # Пытаемся получить JSON-ответ, если это возможно
        try:
            result = res.json()
        except ValueError:
            result = res.text

        return status, result

    def delete_pet(self, auth_key, pet_id):
        path = {'pet_id': pet_id}
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(f'{self.base_url}api/pets/{pet_id}', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except ValueError:
            result = res.text
            return status, result
