import sys
import os
import pytest
import requests
from urls import BASE_URL
from endpoints import Endpoints
from helpers import register_new_courier_and_return_login_password, delete_courier, generate_unique_user
from data import TestData

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture
def courier_credentials():
    """
    Фикстура для создания курьера и получения его учетных данных
    """
    login, password = register_new_courier_and_return_login_password()
    return {"login": login, "password": password}

@pytest.fixture
def order_payload():
    """
    Фикстура для создания тестового заказа
    """
    return TestData.ORDER_DATA

@pytest.fixture
def courier():
    """
    Фикстура для создания курьера, его авторизации и последующей очистки
    """
    courier_data = register_new_courier_and_return_login_password()
    login_data = TestData.create_login_data(courier_data[0], courier_data[1])
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
    """
    Фикстура для получения альтернативных данных заказа
    """
    return TestData.ALTERNATIVE_ORDER_DATA 