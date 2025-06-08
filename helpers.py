import requests
import random
import string
from urls import BASE_URL
from endpoints import Endpoints

def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(BASE_URL + Endpoints.CREATE_COURIER_EP, data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

def generate_unique_user():
    def gen(length=10):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    return {
        "login": gen(),
        "password": gen(),
        "firstName": gen()
    }

def delete_courier(courier_id):
    response = requests.delete(BASE_URL + Endpoints.DELETE_COURIER_EP.format(id=courier_id))
    return response 