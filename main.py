from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, create_engine

from transactions import get_recent_deposits_by_user, create_transaction, get_all_transactions_by_user, three_most_recent_transactions_by_user
from event import Event
from user import User, create_user
from alert_checks import has_withdrawn_three_times_in_a_row, has_deposited_greater_amounts_consecutively, is_depositing_too_much_too_quickly


sqlite_file_name = "test.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine) 

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

def read_user(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.post("/user")
def create_new_user(user: User, session: SessionDep):
    return create_user(user, session)


@app.post("/event")
async def create_event(event: Event, session: Session = Depends(get_session)):
    if not event.user_id or not event.type.strip() or not event.amount or not event.time:
        raise HTTPException(status_code=403, detail="Invalid Request")
    user = read_user(event.user_id, session)

    transaction_method = event.type.lower()
    is_deposit = transaction_method == 'deposit'
    
    if (not is_deposit and (user.total < 0 or user.total - event.amount < 0)):
        return HTTPException(status_code=403, detail="Insufficient Funds")
    
    transaction = create_transaction(event, user, session, True)
    
    if (not is_deposit):
        user.total -= transaction.amount
    else:
        user.total += transaction.amount
        
        
    session.add(user)
    session.commit()
    session.refresh(user)
    
    alert_codes = []

    if not is_deposit and transaction.amount > 100:
        alert_codes.append(1100)
        
    deposits_by_user = get_recent_deposits_by_user(session, user.id)
    all_transactions_by_user = get_all_transactions_by_user(session, user.id)
    three_most_recent_transactions = three_most_recent_transactions_by_user(session, user.id)
    
    if has_withdrawn_three_times_in_a_row(transactions=three_most_recent_transactions):
        alert_codes.append(30)
    if has_deposited_greater_amounts_consecutively(transactions=deposits_by_user):
        alert_codes.append(300)
    if is_depositing_too_much_too_quickly(transactions=all_transactions_by_user):
        alert_codes.append(123)
        
        
    response = {
        "user_id": user.id,
        "alert": bool(alert_codes),
        "alert_codes": alert_codes
    }
    
    return response
    