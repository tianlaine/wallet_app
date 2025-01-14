"""Данный файл нужен для определения структуры базы данных, тут описываются таблицы как python-классы (модели)"""


# Импортируем `create_engine` для подключения к базе данных и
# `Column`, `Integer`, `String` для описания столбцов таблицы.
from sqlalchemy import create_engine, Column, Integer, String

# Импортируем тип для колонки `uuid`
from sqlalchemy.dialects.postgresql import UUID

# Импортируем `declarative_base`, чтобы создать базовый класс для всех моделей.
from sqlalchemy.orm import declarative_base
# Импортируем функцию `uuid4`, чтобы генерировать уникальные идентификаторы (UUID) для кошельков.
from uuid import uuid4

# URL подключения к базе данных PostgreSQL.
DATABASE_URL = "postgresql://user:password@localhost:5432/wallet_db"

# Создаем объект `engine`, который представляет подключение к базе данных.
engine = create_engine(DATABASE_URL)
# Создаем базовый класс `Base` для определения моделей.
Base = declarative_base()

class Wallet(Base): # Представляет таблицу wallets в базе данных.
    __tablename__ = "wallets" # Название таблицы в базе данных.
    id = Column(Integer, primary_key=True, index=True) # первичный ключ таблицы.
    uuid = Column(UUID(as_uuid=True), unique=True, index=True, nullable=False) # уникальный идентификатор кошелька.
    balance = Column(Integer, default=0) # текущий баланс кошелька.