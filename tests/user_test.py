from app.user import User, create_user, read_user


def test_create_user_success(test_session):
    user = User(name="Alice", total=100.0)
    created_user = create_user(user, test_session)
    
    assert created_user is not None
    assert created_user.id is not None
    assert created_user.name == "Alice"
    assert created_user.total == 100.0

def test_create_user_duplicate_id(test_session):
    user1 = User(id=1, name="Bob", total=50.0)
    user2 = User(id=1, name="Charlie", total=75.0)  # Same ID

    create_user(user1, test_session)
    result = create_user(user2, test_session)

    assert result is None  # Should return None due to IntegrityError

def test_read_user_found(test_session):
    user = User(name="Daisy", total=25.5)
    created_user = create_user(user, test_session)
    
    found_user = read_user(created_user.id, test_session)

    assert found_user is not None
    assert found_user.name == "Daisy"
    assert found_user.total == 25.5

def test_read_user_not_found(test_session):
    user = read_user(999, test_session)
    assert user is None