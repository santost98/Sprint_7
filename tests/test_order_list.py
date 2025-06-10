import requests
import allure
from endpoints import Endpoints
from urls import BASE_URL

class TestOrderList:

    @allure.title("Получение списка заказов")
    def test_get_order_list_returns_orders_list(self):
        response = requests.get(BASE_URL + Endpoints.GET_ORDER_LIST_EP)
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list) 