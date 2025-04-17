from sqlmodel import Field, Session, SQLModel, select
from typing import List

from event import Event
from user import User

class Transaction(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    user_id: int | None = Field(foreign_key="user.id")
    amount: float 
    is_success: bool | None = Field(default=False)
    time: int
    transaction_type: str
    
def create_transaction(event: Event, user: User, session: Session, is_success: bool) -> Transaction:
    transaction = Transaction(
        user_id=user.id,
        amount=event.amount,
        time=event.time,
        transaction_type=event.type,
        is_success=is_success  # assuming if you're creating it, it's successful
    )

    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return transaction

def get_recent_deposits_by_user(session: Session, user_id: int) -> List[Transaction]:
    statement = (
        select(Transaction)
        .where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == 'deposit'
        )
        .order_by(Transaction.id.desc())
        .limit(3)
    )
        
    return session.exec(statement).all()

def get_all_transactions_by_user(session: Session, user_id: int) -> List[Transaction]:
    statement = (
        select(Transaction)
        .where(
            Transaction.user_id == user_id,
        )
        .order_by(Transaction.id.desc())
    )
        
    return session.exec(statement).all()

def three_most_recent_transactions_by_user(session: Session, user_id: int) ->List[Transaction]:
    statement = (
        select(Transaction)
        .where(
            Transaction.user_id == user_id,
        )
        .order_by(Transaction.id.desc())
        .limit(3)
    )
        
    return session.exec(statement).all()