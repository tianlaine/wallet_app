"""Данный файл со схемами помогает определить, как данные должны выглядеть (структура, типы)."""


from pydantic import BaseModel # Импортируем базовый класс `BaseModel` из Pydantic.
from enum import Enum # Импортируем `Enum` для создания перечислений.
from uuid import UUID # Импортируем тип данных `UUID` для работы с уникальными идентификаторами.

class OperationType(str, Enum): # Определяет два типа операций для кошелька
    DEPOSIT = "DEPOSIT" # Тип операции: пополнение кошелька.
    WITHDRAW = "WITHDRAW" # Тип операции: снятие средств с кошелька.

class OperationSchema(BaseModel): # Описывает структуру данных для операций с кошельком.
    operationType: OperationType # Поле для указания типа операции (DEPOSIT или WITHDRAW).
    amount: int  # Поле для указания суммы операции.

class WalletSchema(BaseModel): # Описывает структуру данных для представления информации о кошельке.
    uuid: UUID # Уникальный идентификатор кошелька.
    balance: int # Текущий баланс кошелька.

    class Config:
        from_attributes = True  # Включает поддержку работы с объектами SQLAlchemy