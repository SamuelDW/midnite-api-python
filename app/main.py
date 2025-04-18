from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from app.transactions import create_transaction, get_transactions_by_user
from app.request_data import RequestData
from app.user import User, create_user, read_user
from app.alert_checks import has_withdrawn_three_times_in_a_row, has_deposited_greater_amounts_consecutively, is_depositing_too_much_too_quickly
from app.database import create_db_and_tables, SessionDep, get_session


app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.post("/user")
def create_new_user_in_db(user: User, session: SessionDep):
    new_user = create_user(user, session)
    if new_user is None:
        raise HTTPException(status_code=400, detail='Could not create user. Required fields are name and total')
    
    return new_user


@app.post("/event")
async def create_event(request_data: RequestData, session: Session = Depends(get_session)):
    if not request_data.user_id or not request_data.type.strip() or not request_data.amount or not request_data.time:
        raise HTTPException(status_code=403, detail="Invalid Request")
    user = read_user(request_data.user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    transaction_method = request_data.type.lower()
    is_deposit = transaction_method == 'deposit'
    
    if (not is_deposit and (user.total < 0 or user.total - request_data.amount < 0)):
        return HTTPException(status_code=403, detail="Insufficient Funds")
    
    transaction = create_transaction(request_data, user, session, True)
    
    if transaction is None:
        raise HTTPException(status_code=400, detail='Could not save transaction')
    
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
        
    deposits_by_user = get_transactions_by_user(session, user.id, transaction_type='deposit', limit=3)
    all_transactions_by_user = get_transactions_by_user(session, user.id)
    three_most_recent_transactions = get_transactions_by_user(session, user.id, limit=3)
    
    if has_withdrawn_three_times_in_a_row(transactions=three_most_recent_transactions):
        alert_codes.append(30)
    if has_deposited_greater_amounts_consecutively(transactions=deposits_by_user):
        alert_codes.append(300)
    # if the transaction is a withdrawal, shouldn't check I think
    if transaction.transaction_type == 'deposit' and is_depositing_too_much_too_quickly(transactions=all_transactions_by_user):
        alert_codes.append(123)
        
        
    response = {
        "user_id": user.id,
        "alert": bool(alert_codes),
        "alert_codes": alert_codes
    }
    
    return response
    