import pytest
import requests
import allure
import time
from endpoints import Endpoints
from urls import BASE_URL

class TestLoginCourier:

    @allure.title("Успешный логин курьера")
    def test_login_success(self, courier):
        credentials = {"login": courier["login"], "password": courier["password"]}
        response = requests.post(BASE_URL + Endpoints.LOGIN_COURIER_EP, json=credentials)
        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Ошибка при логине без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, courier, missing_field):
        credentials = {"login": courier["login"], "password": courier["password"]}
        credentials.pop(missing_field)
        response = requests.post(BASE_URL + Endpoints.LOGIN_COURIER_EP, json=credentials)
        assert response.status_code in [400, 504]
        if response.status_code == 400:
            assert "message" in response.json()
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка при логине с неверным паролем")
    def test_login_wrong_password(self, courier):
        credentials = {"login": courier["login"], "password": "wrongpass"}
        response = requests.post(BASE_URL + Endpoints.LOGIN_COURIER_EP, json=credentials)
        assert response.status_code == 404
        assert "message" in response.json()
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Ошибка при логине несуществующего пользователя")
    def test_login_nonexistent_user(self):
        credentials = {
            "login": "nonexistent_login_123",
            "password": "nonexistent_password_456"
        }
        response = requests.post(BASE_URL + Endpoints.LOGIN_COURIER_EP, json=credentials)
        assert response.status_code == 404
        assert "message" in response.json()
        assert response.json()["message"] == "Учетная запись не найдена" 