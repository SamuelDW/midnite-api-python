
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.exc import IntegrityError

from app.user import User, create_user, read_user  

@pytest.fixture
def session():
    # In-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_user_success(session):
    user = User(name="Alice", total=100.0)
    created_user = create_user(user, session)
    
    assert created_user is not None
    assert created_user.id is not None
    assert created_user.name == "Alice"
    assert created_user.total == 100.0

def test_create_user_duplicate_id(session):
    user1 = User(id=1, name="Bob", total=50.0)
    user2 = User(id=1, name="Charlie", total=75.0)  # Same ID

    create_user(user1, session)
    result = create_user(user2, session)

    assert result is None  # Should return None due to IntegrityError

def test_read_user_found(session):
    user = User(name="Daisy", total=25.5)
    created_user = create_user(user, session)
    
    found_user = read_user(created_user.id, session)

    assert found_user is not None
    assert found_user.name == "Daisy"
    assert found_user.total == 25.5

def test_read_user_not_found(session):
    user = read_user(999, session)
    assert user is None