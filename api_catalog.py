import requests
import json
import datetime
import functools
from requests_toolbelt.multipart.encoder import MultipartEncoder

def logger(func):
    def wrapper(*args):
        func_res, status, f_res = func(*args)
        # file_head = func_res.requests.headers
        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write(f'\n--\n--\nТестовая сессия началась - {datetime.datetime.now()}')
            file.write('\n\nREQUEST DATA:\n')
            file.write(f'\nПуть запроса: \n{func_res["path"]}\n-----')
            file.write(f'\nMethod запроса: \n{func_res["method"]}\n-----')
            file.write(f'\nЗаголовки запроса: \n{func_res["headers"]}\n-----')
            file.write(f'\nДанные запроса: \n{func_res["data"]}\n')
            file.write(f'\n\nRESPONSE DATA:\n|\nv')
            file.write(f'\nСтатус ответа: {status}')
            file.write(f'\nТело ответа: {func_res["response"]}\n\n')
        return func(*args)
    return wrapper


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод отправляет запрос к API; возвращает статус и результата в установленных переменных 
        в формате json с уникальным ключом пользователя, найденным по отправленным email и password"""

        headers = {
            'accept': 'application/json',
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        print(email, '\n', password, '\n', result)
        return status, result

    @logger
    def get_list_of_pest(self, auth_key: json, filter: str) -> json:
        """Метод отправляет завпрос к API с ключом пользователя и возварщает спсиок питомцев с учётом
        параметров filter"""
        header = {
            'accept': 'application/json',
            'auth_key': auth_key
        }
        filter = {
            'filter': filter
        }

        res = requests.get(self.base_url + 'api/pets', headers=header, params=filter)
        status = res.status_code
        result = ""
        req_data = {
            'headers': header,
            'data': filter,
            'response': res.content,
            'path': res.url,
            'method': res.request
        }
        try:
            result = res.json()
        except:
            result = res.text
        # print(f"\nДлина списка питомцев: {len(result['pets'])}, \n", result)
        print(result)
        return req_data, status, result

    def post_newPet(self, auth_key: json, name: str, pet_type: str, age: str, pet_photo: str) -> json:
        ''''Добавляет питомца через отправку запроса к API;
        вводим строковые данные: имя, статус и фото_урл'''

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': pet_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'accept': 'application/json',
                   'auth_key': auth_key,
                   'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        # print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_ID: str) -> json:
        '''Метод удаляет питомца. Принмает ID, также нужен уникальный API_key'''
        header = {
            'accept': 'application/json',
            'auth_key': auth_key
        }
        res = requests.delete(self.base_url + f'api/pets/{pet_ID}', headers=header)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result

    @logger
    def create_simple_pet(self, auth_key: json, name: str, pet_type: str, age: str) -> json:
        '''Метод создаёт простого питомца без фотографии. Принмает имя, тип питомца, возроаст'''
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': pet_type,
                'age': age
            })
        header = {
            'accept': 'application/json',
            'auth_key': auth_key,
            'Content-Type': data.content_type
        }


        res = requests.post(self.base_url + 'api/create_pet_simple', headers=header, data=data)
        status = res.status_code
        result = ""
        req_params = {
            'headers': header,
            'data': data,
            'response': res.content,
            'path': res.url,
            'method': res.request
        }
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return req_params, status, result

    def upload_photo(self, auth_key: json, pet_ID: str, pet_photo: str) -> json:
        '''Метод загружает фотографию к созданному питомцу. Передаёт ключ АПИ, ай-ди питомца и фото'''

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        header = {'accept': 'application/json',
                  'auth_key': auth_key,
                  'Content-Type': data.content_type
                  }
        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_ID}',
                            headers=header, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        # print(result)
        return status, result

    def put_info_update_pet(self, auth_key: json, pet_ID: str, name: str, pet_type: str, age: str) -> json:
        '''Метод обновляет данные конкретног питомца. Принимает ключ АПИ, айди питомца и новые данные:
        имя, тип питомца, возраст'''

        header = {
            'accept': 'application/json',
            'auth_key': auth_key
        }
        data = {
            'name': name,
            'animal_type': pet_type,
            'age': age
        }

        res = requests.put(self.base_url + f'api/pets/{pet_ID}', headers=header, data=json.dumps(data))
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result



'''def decor_logger(func):
    @functools.wraps(func)
    def wrap_logger(*args, **kwargs):
        resp = func(*args, **kwargs)
        resp_head = resp.request.headers
        resp_data = resp.request.content

        # with open('logfile.txt', 'wr', encoding='utf-8') as lf:
        #     lf.write("Start logging",
        #              f"\nDate/time: {datetime.now()}")
        #     lf.write(func.__name__)
        #     lf.write(f'Headers: {resp_head}\n')
        #     lf.write(f'Data in request: {resp_data}\n')
        #     lf.close()

        return print(resp)

    return wrap_logger'''
