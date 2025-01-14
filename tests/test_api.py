"""Данный файл необходим для unit-тестирования API и выявления ошибок.
Для выполнения тестов можно использовать инструмент pytest"""


from fastapi.testclient import TestClient # Импортируем `TestClient` из FastAPI для тестирования API.
from app.main import app # Импортируем объект `app` из основного файла приложения для тестирования его эндпоинтов.

# Создаем экземпляр `TestClient` для выполнения HTTP-запросов к нашему приложению.
client = TestClient(app)

# Проверяет поведение API при попытке получить данные несуществующего кошелька.
def test_wallet_creation():
    # Выполняем GET-запрос к эндпоинту для проверки кошелька с указанным UUID.
    response = client.get("/api/v1/wallets/some-uuid")
    # Убеждаемся, что статус ответа — 404, так как кошелька с таким UUID не существует.
    assert response.status_code == 404

# Проверяет поведение API при выполнении операции с кошельком.
def test_wallet_deposit_operation():
    # Выполняем POST-запрос к эндпоинту операции с указанным UUID и передаём данные операции.
    response = client.post("/api/v1/wallets/some-uuid/operation", json={"operationType": "DEPOSIT", "amount": 1000})
    # Проверяем, что статус ответа — 200, что означает успешное выполнение операции.
    assert response.status_code == 200
    # Убеждаемся, что тело ответа содержит ожидаемое сообщение об успешной операции.
    assert response.json() == {"message": "Операция прошла успешно."}

# Проверяет поведение API при снятии денег с баланса (снятие средств).
def test_wallet_withdrawal_operation():
    # Предполагаем, что на балансе есть 1000 рублей
    balance = 1000
    withdrawal_amount = 500

    # Если на балансе достаточно средств для снятия
    if balance >= withdrawal_amount:
        # Выполняем POST-запрос к эндпоинту операции с указанным UUID и передаём данные операции.
        response = client.post("/api/v1/wallets/some-uuid/operation", json={"operationType": "WITHDRAW", "amount": withdrawal_amount})
        # Проверяем, что статус ответа — 200, что означает успешное выполнение операции.
        assert response.status_code == 200
        # Убеждаемся, что ответ содержит ожидаемое сообщение об успешной операции.
        assert response.json() == {"message": f"Вы сняли средства со счёта на сумму {withdrawal_amount} рублей."}
    else:
        # Если средств недостаточно
        response = client.post("/api/v1/wallets/some-uuid/operation", json={"operationType": "WITHDRAW", "amount": withdrawal_amount})
        # Проверяем, что статус ответа — 404, что означает, что операция не выполнена.
        assert response.status_code == 404
        # Убеждаемся, что ответ содержит ожидаемое сообщение о недостаточности средств.
        assert response.json() == {"message": "Недостаточно средств."}