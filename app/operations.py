"""Данный файл нужен для проверки условий операции, обновления данных и повторного использования"""


# Импортируем `Session` из SQLAlchemy для работы с сессией базы данных.
from sqlalchemy.orm import Session
# Импортируем модель `Wallet`, представляющую таблицу кошельков в базе данных.
from app.models import Wallet
# Импортируем `OperationSchema`, чтобы использовать схему для проверки и обработки операций.
from app.schemas import OperationSchema


# Выполняет операцию (пополнение или снятие) с балансом кошелька.
# Сессия базы данных для выполнения операций.
def process_operation(db: Session, wallet_uuid: str, operation: OperationSchema):
    # Пытаемся найти кошелёк в базе данных по его UUID.
    wallet = db.query(Wallet).filter(Wallet.uuid == wallet_uuid).first()

    # Если кошелёк не найден, возвращаем `False`.
    if not wallet:
        if operation.operationType == "DEPOSIT":
            wallet = Wallet(uuid=wallet_uuid, balance=0)  # Создаем новый кошелек с балансом 0
            db.add(wallet)  # Добавляем новый кошелек в сессию
            db.commit()  # Сохраняем изменения в базе данных
            db.refresh(wallet)  # Обновляем объект `wallet`
        else:
            return False

    # Если тип операции — DEPOSIT (пополнение), увеличиваем баланс кошелька на указанную сумму.
    if operation.operationType == "DEPOSIT":
        wallet.balance += operation.amount
    # Если тип операции — WITHDRAW (снятие средств):
    # Проверяем, хватает ли средств на балансе. Если нет, возвращаем `False`.
    elif operation.operationType == "WITHDRAW":
        if wallet.balance < operation.amount:
            return False
        # Уменьшаем баланс кошелька на указанную сумму.
        wallet.balance -= operation.amount

    # Сохраняем изменения в базе данных.
    db.commit()
    # Обновляем объект `wallet`, чтобы получить актуальные данные после изменений.
    db.refresh(wallet)
    # Возвращаем `True`, если операция успешно выполнена.
    return True