from app.transactions import Transaction, get_transactions_by_user

def test_get_transactions_by_user_basic(test_session):
    # Setup test data
    transactions = [
        Transaction(user_id=1, amount=100, transaction_type="deposit", is_success=True, time=10),
        Transaction(user_id=1, amount=200, transaction_type="withdrawal", is_success=True, time=15),
        Transaction(user_id=1, amount=150, transaction_type="deposit", is_success=True, time=20),
        Transaction(user_id=2, amount=300, transaction_type="deposit", is_success=True, time=25),
    ]

    test_session.add_all(transactions)
    test_session.commit()

    # Test basic fetch
    results = get_transactions_by_user(test_session, user_id=1)
    assert len(results) == 3
    assert results[0].amount == 150  # last deposit added (should be first due to DESC order)
    assert results[-1].amount == 100

def test_get_transactions_with_filter_and_limit(test_session):
    transactions = [
        Transaction(user_id=1, amount=100, transaction_type="deposit", is_success=True, time=10),
        Transaction(user_id=1, amount=200, transaction_type="deposit", is_success=True, time=20),
        Transaction(user_id=1, amount=300, transaction_type="withdrawal", is_success=True, time=30),
    ]
    test_session.add_all(transactions)
    test_session.commit()

    # Only deposits, limit to 1
    results = get_transactions_by_user(test_session, user_id=1, transaction_type="deposit", limit=1)
    assert len(results) == 1
    assert results[0].amount == 200
