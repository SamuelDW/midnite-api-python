from typing import List
from transactions import Transaction

def has_withdrawn_three_times_in_a_row(transactions: List[Transaction]) -> bool:
    if len(transactions) < 3:
        return False

    # Check only the first 3 transactions
    for i in range(3):
        if transactions[i].transaction_type != 'withdrawal':
            return False

    return True

def has_deposited_greater_amounts_consecutively(transactions: List[Transaction]) -> bool:
    if len(transactions) < 3:
        return False

    return (
        transactions[0].amount > transactions[1].amount and
        transactions[1].amount > transactions[2].amount
    )

def is_depositing_too_much_too_quickly(transactions: List[Transaction]) -> bool:
    if not transactions:
        return False

    # If the first deposit is too much, return early
    first = transactions[0]
    if first.amount > 200 and first.transaction_type == 'deposit':
        return True

    total_time = 0
    total_deposit = 0

    for tx in transactions:
        total_time += tx.time
        if tx.transaction_type == 'deposit':
            total_deposit += tx.amount

        if total_time >= 30:
            if total_deposit > 200:
                return True
            else:
                return False

    return False
