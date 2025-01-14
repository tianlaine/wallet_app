# Описание проекта

Данное приложение может принимать два REST-запроса на обновление онлайн-кошелька и проверку баланса
В стеке использовались основные утилиты и библиотеки такие как fastAPI для создания приложения и обработки ошибок, sqlalchemy для подключения к базе данных postgresql и TestClietnt для тестирования

# Запуск через `docker`

Приложение можно запустить через `docker-compose` следующим образом:

```bash
docker-compose build
docker-compose up db
docker-compose up app
```

Последние две команды должны выполняться в разных процессах (разных вкладках терминала)

Если у вас не получается выполнить `docker-compose build` из-за недоступности dockerhub, попробуйте следующее:

```bash
docker pull cr.yandex/mirror/python:3.9-slim
```

# Пример использования

Запросы к сервису можно делать через `curl`

Для пополнения:

```bash
curl -X POST "http://localhost:8000/api/v1/wallets/496aa349-c5fc-40fc-b9f3-9831ce907d50/operation" \
           -H "Content-Type: application/json" \
           -d '{"operationType": "DEPOSIT", "amount": 1000}'
```

Для снятия:

```bash
curl -X POST "http://localhost:8000/api/v1/wallets/496aa349-c5fc-40fc-b9f3-9831ce907d50/operation" \
           -H "Content-Type: application/json" \
           -d '{"operationType": "WITHDRAW", "amount": 500}'
```

Для проверки баланса:

```bash
curl -X GET "http://localhost:8000/api/v1/wallets/496aa349-c5fc-40fc-b9f3-9831ce907d50"
```
