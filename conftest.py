import sys
import os
import pytest
import requests
import random
import string
from urls import BASE_URL
from endpoints import Endpoints
from helpers import register_new_courier_and_return_login_password, delete_courier, generate_unique_user

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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

    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

@pytest.fixture
def courier():
    courier_data = register_new_courier_and_return_login_password()
    login_data = {
        "login": courier_data[0],
        "password": courier_data[1]
    }
    response = requests.post(BASE_URL + Endpoints.LOGIN_COURIER_EP, json=login_data)
    assert response.status_code == 200
    courier_id = response.json()["id"]
    
    yield {
        "id": courier_id,
        "login": courier_data[0],
        "password": courier_data[1]
    }
    
    delete_courier(courier_id)

@pytest.fixture
def order_data():
    return {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "Москва, ул. Пушкина, д. 10",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-03-20",
        "comment": "Позвонить за час до доставки"
    } 