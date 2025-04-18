from sqlmodel import Field, Session, SQLModel, select
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from app.request_data import RequestData
from app.user import User

class Transaction(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    user_id: int | None = Field(foreign_key="user.id")
    amount: float 
    is_success: bool | None = Field(default=False)
    time: int
    transaction_type: str
    
def create_transaction(event: RequestData, user: User, session: Session, is_success: bool) -> Transaction|None:
    transaction = Transaction(
        user_id=user.id,
        amount=event.amount,
        time=event.time,
        transaction_type=event.type,
        is_success=is_success  # assuming if you're creating it, it's successful
    )
    try:   
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
    except IntegrityError:
        session.rollback()
        return None

    return transaction

def get_transactions_by_user(
    session: Session,
    user_id: int,
    transaction_type: Optional[str] = None,
    limit: Optional[int] = None
) -> List[Transaction]:
    statement = select(Transaction).where(Transaction.user_id == user_id)

    if transaction_type:
        statement = statement.where(Transaction.transaction_type == transaction_type)

    statement = statement.order_by(Transaction.id.desc())

    if limit:
        statement = statement.limit(limit)

    return session.exec(statement).all()