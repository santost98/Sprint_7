import pytest
import requests
import allure
from endpoints import Endpoints
from urls import BASE_URL

class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цветов")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_colors(self, colors):
        order_data = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Москва, ул. Пушкина, д. 10",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-03-20",
            "comment": "Позвонить за час",
            "color": colors
        }
        response = requests.post(BASE_URL + Endpoints.CREATE_ORDER_EP, json=order_data)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int) 