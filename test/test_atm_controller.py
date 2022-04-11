import unittest
from unittest import TestCase
from unittest.mock import patch

from atm_controller import *
# from atm_controller import Session, restart_session
# from atm_hardware_driver import get_card_number


# @patch('atm_hardware_driver.get_card_number')
_card_number = ''


def dispatch_card_number(card_number):
    # return card_number
    global _card_number
    _card_number = card_number


def dispatched_card_number():
    return _card_number


class Case:

    def __init__(self, card_number: str, pin: str, balance: int):
        self.card_number = card_number
        self.pin = pin
        self.balance = balance


class TestSession(TestCase):

    def setUp(self):
        self.cases = (
            Case(card_number='123-456', pin='0954', balance=300),
            Case(card_number='178-982', pin='1059', balance=500),
            Case(card_number='632-777', pin='3582', balance=100),
        )
        self.sessions = [Session() for _ in range(len(self.cases))]

    def tearDown(self):
        pass

    @patch('atm_controller.get_card_number', dispatched_card_number)
    def test_read_card(self):
        # def test_auth(self):
        for i, (case, session) in enumerate(zip(self.cases, self.sessions)):
            with self.subTest(i=i):
                # insert card
                dispatch_card_number(case.card_number)
                assert _card_number == case.card_number
                session.read_card()

                assert session._card_number == case.card_number
                self.assertEqual(session._card_number, case.card_number)

                # # get authorization

            # restart_session()

    def test_select_account(self):
        pass

    def test_balance_check(self):
        pass

    def test_deposit(self):
        pass

    def test_withdraw(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
