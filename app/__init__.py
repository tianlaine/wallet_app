'''Данный файл используется для инициализации пакета Python'''


from app.models import Wallet # Модель Wallet, представляющая таблицу кошельков
from app.schemas import WalletSchema, OperationSchema # Схемы для валидации входных данных и описания структуры ответов
from app.operations import process_operation # Функция для обработки операций (пополнение/снятие)
from app.db import SessionLocal, engine # Импортируем локальную сессию для работы с базой данных и объект engine для подключения