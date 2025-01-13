'''Данный файл используется для хранения конфигурации параметров приложения'''


import os  # Модуль os используется для работы с переменными окружения.
from dotenv import load_dotenv  # Импортируем функцию load_dotenv для загрузки переменных окружения из .env-файла.

"""
Загрузка переменных окружения из .env-файла. 
Эта строка загружает переменные окружения из файла `.env` в корне проекта.
Переменные окружения, заданные в .env, становятся доступными через os.getenv().
"""
load_dotenv()

"""
Класс Config содержит настройки приложения.
Все параметры вынесены в этот класс для удобства изменения и чтения конфигураций.
"""
class Config:
    # Основные параметры приложения
    # Название приложения, используется для логирования или отображения на главной странице.
    APP_NAME = "WalletApp"

    # Флаг режима отладки. Если переменная окружения DEBUG = "true" или "1", режим отладки включается.
    # По умолчанию используется значение "False".
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")

    # Секретный ключ, используемый для криптографических операций, таких как подпись JWT или CSRF-токенов.
    # Значение по умолчанию — "super-secret-key", но в production его нужно обязательно заменить.
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    # Настройки базы данных
    # Имя пользователя базы данных, по умолчанию "postgres".
    DB_USER = os.getenv("DB_USER", "postgres")

    # Пароль для подключения к базе данных. По умолчанию используется "123".
    DB_PASSWORD = os.getenv("DB_PASSWORD", "123")

    # Хост базы данных. Локальный сервер по умолчанию — "localhost".
    DB_HOST = os.getenv("DB_HOST", "localhost")

    # Порт подключения к базе данных PostgreSQL, по умолчанию 5432.
    DB_PORT = os.getenv("DB_PORT", "5432")

    # Имя базы данных. По умолчанию используется "postgres".
    DB_NAME = os.getenv("DB_NAME", "postgres")

    # Формируем строку подключения к базе данных в формате, который поддерживает SQLAlchemy.
    # Она объединяет пользователя, пароль, хост, порт и имя базы данных.
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Другие параметры приложения
    # Максимальное количество подключений к базе данных. Значение по умолчанию — 10.
    MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", 10))

    # Минимальное количество подключений к базе данных. Значение по умолчанию — 1.
    MIN_CONNECTIONS = int(os.getenv("MIN_CONNECTIONS", 1))

    # Переменная среды, указывающая режим работы приложения: development, production и т.д.
    # По умолчанию — "development".
    ENV = os.getenv("ENV", "development")