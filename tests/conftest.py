from sqlmodel import SQLModel, Session, create_engine
import pytest

# from tr import Transaction

@pytest.fixture
def test_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session