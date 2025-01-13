'''Данный файл используется для запуска приложения, настройки базы данных и обработки запросов'''


from app.db import SessionLocal, engine  # Импортируем локальную сессию для работы с базой данных и объект engine для подключения
from app.config import Config  # Конфигурация приложения, где хранятся параметры, такие как URL базы данных
from app.models import Wallet  # Модель Wallet, представляющая таблицу кошельков
from app.operations import process_operation  # Функция для обработки операций (пополнение/снятие)
from app.schemas import WalletSchema, OperationSchema  # Схемы для валидации входных данных и описания структуры ответов
from app.models import Base  # Базовый класс моделей SQLAlchemy для работы с таблицами

from fastapi import FastAPI, HTTPException, Depends  # Основные элементы FastAPI для создания приложения и обработки ошибок
from sqlalchemy import create_engine  # Создание движка подключения к базе данных
from sqlalchemy.orm import Session, sessionmaker  # Управление сессиями для взаимодействия с базой данных
from uuid import UUID  # Тип данных для универсального идентификатора кошельков

"""
Инициализация базы данных.
sessionmaker создает объект для управления сессиями:
- autocommit=False: изменения в базе не подтверждаются автоматически
- autoflush=False: изменения не отправляются автоматически перед запросом
- bind=engine: сессия связана с конкретным движком
"""
DATABASE_URL = Config.SQLALCHEMY_DATABASE_URL  # URL подключения к базе данных, заданный в конфигурации
engine = create_engine(DATABASE_URL)  # Создаем движок подключения к базе данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем приложение FastAPI
app = FastAPI()

# Эндпоинт для проверки статуса приложения
@app.get("/")
def read_root():
    # Возвращает название приложения и флаг режима отладки
    return {"app_name": Config.APP_NAME, "debug": Config.DEBUG}

"""
Создание всех таблиц в базе данных
Используется для создания таблиц на основе моделей, если их ещё нет в базе данных
"""
Base.metadata.create_all(bind=engine)

"""
Зависимость для работы с базой данных.
Создает сессию для работы с базой данных.
Оборачивает выполнение запроса в блок try-finally для автоматического закрытия сессии.
"""
def get_db():

    db = SessionLocal()  # Создаем новую сессию
    try:
        yield db  # Передаем управление вызову сессии
    finally:
        db.close()  # После завершения запроса закрываем сессию

""" 
Эндпоинт для выполнения операций с кошельком (пополнение или снятие)
Выполняет операцию DEPOSIT или WITHDRAW для кошелька.
- wallet_uuid: UUID кошелька
- operation: Данные операции, переданные в теле запроса
- db: Сессия базы данных, передается через Depends
"""
@app.post("/api/v1/wallets/{wallet_uuid}/operation")
def wallet_operation(wallet_uuid: UUID, operation: OperationSchema, db: Session = Depends(get_db)):
    # Выполняем обработку операции через функцию process_operation
    result = process_operation(db, wallet_uuid, operation)
    if not result:
        # Если операция некорректна (например, недостаточно средств), возвращаем ошибку
        raise HTTPException(status_code=400, detail="Неверный тип операции или недостаточно средств на счёте.")
    # Возвращаем успешное выполнение операции
    return {"message": "Операция прошла успешно."}

"""
Эндпоинт для получения баланса кошелька.
Получает баланс кошелька.
- wallet_uuid: UUID кошелька
- db: Сессия базы данных, передается через Depends
"""
@app.get("/api/v1/wallets/{wallet_uuid}", response_model=WalletSchema)
def get_balance(wallet_uuid: UUID, db: Session = Depends(get_db)):
    # Выполняем запрос для поиска кошелька по UUID
    wallet = db.query(Wallet).filter(Wallet.uuid == wallet_uuid).first()
    if not wallet:
        # Если кошелек не найден, возвращаем ошибку 404
        raise HTTPException(status_code=404, detail="Кошелёк не найден.")
    # Возвращаем информацию о кошельке в формате JSON, автоматически сериализуемом FastAPI
    return wallet