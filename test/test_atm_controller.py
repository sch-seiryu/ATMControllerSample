import unittest
from unittest import TestCase
from unittest.mock import patch

from atm_controller import *


# region WRAPPER_TO_PATCH
_wrapped_value = None


def set_wrapped_value(value):
    global _wrapped_value
    _wrapped_value = value


def get_wrapped_value():
    return _wrapped_value


def compare_with_wrapped_value(*value):
    return value == _wrapped_value


class ValueWrapper:

    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value
# endregion WRAPPER_TO_PATCH


class Case:  # DTO for sample cases.

    def __init__(self, card_number: str, pin: str, accounts: dict):
        self.card_number = card_number
        self.pin = pin
        self.accounts = accounts  # <K, V>: <account_number, balance>


class TestSession(TestCase):

    def setUp(self):
        self.cases = (
            Case(card_number='123-456', pin='0954', accounts={'AB1514': 500}),
            Case(card_number='178-982', pin='1059', accounts={'AB3000': 300, 'BC1052': 80}),
            Case(card_number='632-777', pin='3582', accounts={'AA1243': 100, 'BB1845': 50, 'CC9428': 200}),
        )
        self.sessions = [Session() for _ in range(len(self.cases))]

    @patch('atm_controller.request_authorization', compare_with_wrapped_value)
    @patch('atm_hardware_driver.get_card_number', get_wrapped_value)
    def test_auth(self):
        for i, (case, session) in enumerate(zip(self.cases, self.sessions)):
            with self.subTest(i=i):
                # region INSERT_CARD

                # Card inserted - load card number in the patcher, and read card number in a session.
                set_wrapped_value(case.card_number)
                session.read_card()

                # Test reading of card number.
                self.assertEqual(session._card_number, case.card_number)

                # Test exception raises if already card number has been read.
                self.assertRaises(InvalidSessionException, session.read_card)

                # Test a case of incorrect PIN.
                self.assertRaises(InvalidPinNumberException, session.authorize, ('abcd',))
                self.assertRaises(InvalidPinNumberException, session.authorize, ('0000',))
                # - Note that '0000' is unable to be used as PIN.
                self.assertFalse(session._auth)
                # endregion INSERT_CARD

                # region PIN_AUTHORIZATION

                # Test a case of correct PIN.
                # Note - when the PIN is correct, session get auth, thus no more calling of 'authorize()' is acceptable.
                set_wrapped_value((case.card_number, case.pin))
                self.assertEqual((session._card_number, case.pin), get_wrapped_value())
                session.authorize(case.pin)
                self.assertTrue(session.auth)

                # Test a case of re-do authorization.
                self.assertRaises(InvalidSessionException, session.authorize, (case.pin,))
                # endregion PIN_AUTHORIZATION

    def test_account_management(self):
        # region SELECT_ACCOUNT

        # endregion SELECT_ACCOUNT

        # region DEPOSIT

        # endregion DEPOSIT
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)

    # TODO @Deprecated (it didn't work as I intended)
    # # Making a suite of tests
    # suite = unittest.TestSuite()
    # suite.addTest(TestSession('test_read_card'))
    # suite.addTest(TestSession('test_authorize'))
    #
    # # Run test with custom runner, instead of generic start.
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
