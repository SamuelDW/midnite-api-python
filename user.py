from sqlmodel import Field, Session, SQLModel, select

class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    total: float | None = Field(default=0)
    
def create_user(user: User, session: Session) -> User:

    session.add(user)
    session.commit()
    session.refresh(user)
    return user