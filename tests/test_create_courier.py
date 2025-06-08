import pytest
import requests
import allure
from endpoints import Endpoints
from urls import BASE_URL
from helpers import generate_unique_user

class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        courier_data = generate_unique_user()
        response = requests.post(BASE_URL + Endpoints.CREATE_COURIER_EP, json=courier_data)
        assert response.status_code == 201
        assert response.json()["ok"] == True

    @allure.title("Ошибка при создании курьера с существующим логином")
    def test_create_duplicate_courier(self, courier):
        duplicate_data = {
            "login": courier["login"],
            "password": "different_password",
            "firstName": "different_name"
        }
        response = requests.post(BASE_URL + Endpoints.CREATE_COURIER_EP, json=duplicate_data)
        assert response.status_code == 409
        assert "message" in response.json()
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field):
        courier_data = generate_unique_user()
        courier_data.pop(missing_field)
        response = requests.post(BASE_URL + Endpoints.CREATE_COURIER_EP, json=courier_data)
        assert response.status_code == 400
        assert "message" in response.json()
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Ошибка при создании курьера с одинаковым логином и разным паролем")
    def test_create_courier_same_login_different_password(self, courier):
        duplicate_data = {
            "login": courier["login"],
            "password": "different_password",
            "firstName": "different_name"
        }
        response = requests.post(BASE_URL + Endpoints.CREATE_COURIER_EP, json=duplicate_data)
        assert response.status_code == 409
        assert "message" in response.json()
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой." 