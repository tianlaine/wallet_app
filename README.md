# Описание проекта

Данное приложение может принимать два REST-запроса на снятие и пополнение счёта онлайн-кошелька.
В стеке использовались основные утилиты и библиотеки такие как fastAPI для создания приложения и обработки ошибок, sqlalchemy для подключения к базе данных postgresql и TestClient для тестирования.

# Запуск через `docker`

Приложение можно запустить через `docker-compose` следующим образом:

```bash
docker-compose build
docker-compose up db
docker-compose up app
```

Последние две команды должны выполняться в разных процессах.

Если у вас не получается выполнить `docker-compose build` из-за недоступности dockerhub, попробуйте следующее:

```bash
docker pull cr.yandex/mirror/python:3.9-slim
docker pull cr.yandex/mirror/python:3.9-slim
```









