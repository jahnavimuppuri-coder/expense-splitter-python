import pytest

from app.settle import (
    SettleError,
    balances,
    settle,
    split_evenly,
    to_paise,
    total_moved,
)


def test_split_100_rupees_three_people():
    shares = split_evenly(10000, 3)

    assert shares == [3334, 3333, 3333]
    assert sum(shares) == 10000


def test_split_remainder_goes_to_earliest_shares():
    shares = split_evenly(10, 4)

    assert shares == [3, 3, 2, 2]
    assert sum(shares) == 10


def test_split_one_paisa_between_three_people():
    assert split_evenly(1, 3) == [1, 0, 0]


def test_split_between_zero_people_is_rejected():
    with pytest.raises(SettleError):
        split_evenly(100, 0)


def test_convert_rupees_to_paise():
    assert to_paise(100) == 10000
    assert to_paise("12.50") == 1250


@pytest.mark.parametrize("amount", [0, -1, "invalid", None])
def test_invalid_amount_is_rejected(amount):
    with pytest.raises(SettleError):
        to_paise(amount)


def test_balances_for_one_bill():
    bills = [
        {
            "payer": 1,
            "amount": 10000,
            "shares": {1: 3334, 2: 3333, 3: 3333},
        }
    ]

    assert balances(bills) == {1: 6666, 2: -3333, 3: -3333}


def test_incorrect_bill_share_total_is_rejected():
    bills = [
        {
            "payer": 1,
            "amount": 10000,
            "shares": {1: 3333, 2: 3333, 3: 3333},
        }
    ]

    with pytest.raises(SettleError):
        balances(bills)


def test_settlement_payments_balance_exactly():
    bills = [
        {
            "payer": 1,
            "amount": 10000,
            "shares": {1: 3334, 2: 3333, 3: 3333},
        }
    ]

    payments = settle(bills)

    assert sum(payment["paise"] for payment in payments) == 6666
    assert all(payment["paise"] > 0 for payment in payments)
    assert total_moved(payments) == 6666


def test_no_payment_needed_when_there_are_no_bills():
    assert settle([]) == []
    assert total_moved(settle([])) == 0
