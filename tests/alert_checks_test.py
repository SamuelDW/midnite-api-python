from app.alert_checks import (
    has_withdrawn_three_times_in_a_row,
    has_deposited_greater_amounts_consecutively,
    is_depositing_too_much_too_quickly,
)

class MockTransaction:
    def __init__(self, transaction_type, amount, time):
        self.transaction_type = transaction_type
        self.amount = amount
        self.time = time

# --- Tests for has_withdrawn_three_times_in_a_row ---

def test_withdrawn_three_times_true():
    transactions = [
        MockTransaction('withdrawal', 50, 1),
        MockTransaction('withdrawal', 20, 2),
        MockTransaction('withdrawal', 30, 3),
    ]
    assert has_withdrawn_three_times_in_a_row(transactions) == True

def test_withdrawn_three_times_false_not_all_withdrawals():
    transactions = [
        MockTransaction('withdrawal', 50, 1),
        MockTransaction('deposit', 20, 2),
        MockTransaction('withdrawal', 30, 3),
    ]
    assert has_withdrawn_three_times_in_a_row(transactions) == False

def test_withdrawn_three_times_false_less_than_three():
    transactions = [
        MockTransaction('withdrawal', 50, 1),
        MockTransaction('withdrawal', 20, 2),
    ]
    assert has_withdrawn_three_times_in_a_row(transactions) == False

# --- Tests for has_deposited_greater_amounts_consecutively ---

def test_deposited_greater_amounts_true():
    transactions = [
        MockTransaction('deposit', 300, 1),
        MockTransaction('deposit', 200, 2),
        MockTransaction('deposit', 100, 3),
    ]
    assert has_deposited_greater_amounts_consecutively(transactions) == True

def test_deposited_greater_amounts_false_not_decreasing():
    transactions = [
        MockTransaction('deposit', 100, 1),
        MockTransaction('deposit', 200, 2),
        MockTransaction('deposit', 300, 3),
    ]
    assert has_deposited_greater_amounts_consecutively(transactions) == False

def test_deposited_greater_amounts_false_less_than_three():
    transactions = [
        MockTransaction('deposit', 300, 1),
        MockTransaction('deposit', 200, 2),
    ]
    assert has_deposited_greater_amounts_consecutively(transactions) == False

# --- Tests for is_depositing_too_much_too_quickly ---

def test_depositing_too_much_first_transaction():
    transactions = [
        MockTransaction('deposit', 250, 5),
        MockTransaction('deposit', 50, 5),
    ]
    assert is_depositing_too_much_too_quickly(transactions) == True

def test_depositing_too_much_within_30_seconds():
    transactions = [
        MockTransaction('deposit', 100, 10),
        MockTransaction('deposit', 150, 10),
        MockTransaction('withdrawal', 50, 10),
    ]
    assert is_depositing_too_much_too_quickly(transactions) == True

def test_not_depositing_too_much_total_under_200():
    transactions = [
        MockTransaction('deposit', 80, 10),
        MockTransaction('deposit', 90, 15),
        MockTransaction('withdrawal', 50, 10),
    ]
    assert is_depositing_too_much_too_quickly(transactions) == False


def test_empty_transactions():
    assert is_depositing_too_much_too_quickly([]) == False
