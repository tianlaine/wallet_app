"""Данный файл используется для подключения к базе данных и управления сессиями"""


# Импортируем `create_engine` из SQLAlchemy для создания подключения к базе данных.
from sqlalchemy import create_engine
# Импортируем `sessionmaker`, чтобы создавать сессии для взаимодействия с базой данных.
from sqlalchemy.orm import sessionmaker

# URL для подключения к базе данных PostgreSQL.
DATABASE_URL = "postgresql://postgres:123@localhost:5432/postgres"

# Создаем объект `engine`, который представляет подключение к базе данных.
engine = create_engine(DATABASE_URL, echo=True)
# Создаем фабрику для создания сессий (объектов `Session`), которые используются для работы с базой данных.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)