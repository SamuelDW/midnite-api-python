from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    total: float | None = Field(default=0, ge=0)
    
def create_user(user: User, session: Session) -> User|None:
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        return None
    
def read_user(user_id: int, session: Session) -> User|None:
    user = session.get(User, user_id)
    if not user:
        return None
    return user