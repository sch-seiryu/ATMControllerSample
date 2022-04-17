import unittest
from unittest import TestCase
from unittest.mock import patch

from atm_controller import *


# region WRAPPER_TO_PATCH
_wrapped_value = None  # A temporary placeholder for patched methods.


def set_wrapped_value(value):
    global _wrapped_value
    _wrapped_value = value


def get_wrapped_value(*args):
    return _wrapped_value


def compare_with_wrapped_value(*value):
    return value == _wrapped_value


def neutralizer_wrapper(*args, **kwargs):
    """Denies all activities. Mostly used to ignore raising of 'NotImplementedError'.
    
    :return:
    """
    return


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
        self.account_numbers = list(accounts.keys())

        # Notice that the balances are not listed, as it is supposed to be acquired through bank API.

    def account_number_at(self, index):
        return self.account_numbers[index]

    def balance_of(self, account_number):
        return self.accounts[account_number]


class TestSession(TestCase):

    def setUp(self):
        self.cases = (
            Case(card_number='123-456', pin='0954', accounts={'AB1514': 500}),
            Case(card_number='178-982', pin='1059', accounts={'AB3000': 300, 'BC1052': 80}),
            Case(card_number='632-777', pin='3582', accounts={'AA1243': 100, 'BB1845': 50, 'CC9428': 200}),
        )

    @patch('atm_controller.request_authorization', compare_with_wrapped_value)
    @patch('atm_hardware_driver.show_balance', neutralizer_wrapper)
    @patch('atm_hardware_driver.finalize_and_return_card', neutralizer_wrapper)
    @patch('atm_hardware_driver.get_card_number', get_wrapped_value)
    def test_controller(self):
        # TEST - card insertion, and authorization // USING ALL THREE CASES
        # region Preparing sessions...
        CARD_INSERTION_AND_AUTHROIZATION_TEST_COUNTS = 4
        card_sessions = [
            [Session() for _ in range(CARD_INSERTION_AND_AUTHROIZATION_TEST_COUNTS)] for _ in range(len(self.cases))]
        # endregion Preparing sessions...
        for case_number, (case, sessions) in enumerate(zip(self.cases, card_sessions)):
            with self.subTest(test_card_insertion_and_authorization=f'Case{case_number}'):
                # region INSERT_CARD

                # Card inserted - load card number in the patcher, and read card number in a session.
                set_wrapped_value(case.card_number)
                sessions[0].read_card()
                sessions[1].read_card()
                sessions[2].read_card()
                sessions[3].read_card()

                # Test reading of card number.
                self.assertEqual(sessions[0]._card_number, case.card_number)

                # Test exception raises if already card number has been read.
                self.assertRaises(InvalidSessionException, sessions[0].read_card)

                # Test a case of incorrect PIN.
                self.assertRaises(InvalidPinNumberException, sessions[1].authorize, ('abcd',))
                self.assertRaises(InvalidPinNumberException, sessions[2].authorize, ('0000',))
                # - Note that '0000' is unable to be used as PIN.
                self.assertFalse(sessions[1]._auth)
                self.assertFalse(sessions[2]._auth)
                # endregion INSERT_CARD

                # region PIN_AUTHORIZATION

                # Test a case of correct PIN.
                # Note - when the PIN is correct, session get auth, thus no more calling of 'authorize()' is acceptable.
                set_wrapped_value((case.card_number, case.pin))
                self.assertEqual((sessions[3]._card_number, case.pin), get_wrapped_value())
                sessions[3].authorize(case.pin)
                self.assertTrue(sessions[3].auth)

                # Test a case of re-do authorization.
                self.assertRaises(InvalidSessionException, sessions[3].authorize, (case.pin,))
                # endregion PIN_AUTHORIZATION

        # region SELECT_ACCOUNT
        # USING CASE0
        case = self.cases[0]
        # region Preparing sessions...
        TEST_SESSION_COUNTS_FOR_SELECT_ACCOUNT = 3
        sessions = [Session() for _ in range(TEST_SESSION_COUNTS_FOR_SELECT_ACCOUNT)]
        for s in sessions:
            s: Session
            set_wrapped_value(case.card_number)
            s.read_card()
            set_wrapped_value((case.card_number, case.pin))
            s.authorize(case.pin)
        # endregion Preparing sessions...

        with self.subTest('test_select_account'):
            with patch('atm_hardware_driver.select_account_index', get_wrapped_value
                       ), patch('atm_controller.request_accounts', lambda x: list(case.accounts.keys())
                                ), patch('atm_controller.get_balance', lambda x: case.accounts[x]):
                # Test improper account selection
                # - negative index selected
                set_wrapped_value(-1)
                self.assertRaises(InvalidSessionException, sessions[0].select_accounts)
                # - selected index is out of bound
                set_wrapped_value(5)
                self.assertRaises(InvalidSessionException, sessions[1].select_accounts)

                # Test proper account selection
                set_wrapped_value(0)
                sessions[2].select_accounts()
                self.assertEqual(sessions[2]._account, list(case.accounts.keys())[0])

                # Test reselect account prevention
                self.assertRaises(InvalidSessionException, sessions[2].select_accounts)
        # endregion SELECT_ACCOUNT

        # region DEPOSIT
        # USING CASE1
        case = self.cases[1]
        # region Preparing sessions...
        TEST_SESSION_COUNTS_FOR_DEPOSIT = 3
        sessions = [Session() for _ in range(TEST_SESSION_COUNTS_FOR_DEPOSIT)]
        for s in sessions:
            s: Session
            set_wrapped_value(case.card_number)
            s.read_card()
            set_wrapped_value((case.card_number, case.pin))
            s.authorize(case.pin)
        # endregion Preparing sessions...

        with self.subTest('test_deposit'):
            with patch('atm_hardware_driver.deposit', get_wrapped_value
                       ), patch('atm_controller.update_balance', neutralizer_wrapper
                                ), patch('atm_controller.request_accounts', lambda x: case.account_numbers
                                         ), patch('atm_controller.get_balance', lambda x: case.balance_of(x)):
                # Test return value is g.e. than 0
                # - Using first account
                with patch('atm_hardware_driver.select_account_index', get_wrapped_value):
                    set_wrapped_value(0)
                    sessions[0].select_accounts()
                    # deposit negative value
                    set_wrapped_value(-150)
                    self.assertRaises(InvalidSessionException, sessions[0].deposit)
                    # check no change of balance
                    self.assertEqual(sessions[0]._balance, 300)

                # Test balance is properly updated
                # - Using second account
                with patch('atm_hardware_driver.select_account_index', get_wrapped_value):
                    set_wrapped_value(1)
                    sessions[1].select_accounts()
                    # check balance first
                    self.assertEqual(sessions[1]._balance, 80)
                    # deposit proper money
                    set_wrapped_value(222)
                    try:
                        sessions[1].deposit()  # an error may be caught from bank API, due to unaccomplished works.
                    except NotImplementedError:
                        pass
                    self.assertEqual(sessions[1]._balance, 302)  # $80 + $222 = $302
        # endregion DEPOSIT

        # region WITHDRAWAL
        # USING CASE2
        case = self.cases[2]
        # region Preparing sessions...
        TEST_SESSION_COUNTS_FOR_DEPOSIT = 4
        sessions = [Session() for _ in range(TEST_SESSION_COUNTS_FOR_DEPOSIT)]
        for s in sessions:
            s: Session
            set_wrapped_value(case.card_number)
            s.read_card()
            set_wrapped_value((case.card_number, case.pin))
            s.authorize(case.pin)
        # endregion Preparing sessions...
        with self.subTest('test_withdrawal'):
            with patch('atm_hardware_driver.withdrawal_amount', get_wrapped_value
                       ), patch('atm_controller.update_balance', neutralizer_wrapper
                                ), patch('atm_controller.request_accounts', lambda x: case.account_numbers
                                         ), patch('atm_controller.get_balance', lambda x: case.balance_of(x)):

                # TODO the function requires proper value in loop, so different approach is necessary.
                """# Test withdrawal amount is non-positive.
                # - Using first account
                with patch('atm_hardware_driver.select_account_index', get_wrapped_value):
                    set_wrapped_value(0)
                    sessions[0].select_accounts()
                    sessions[1].select_accounts()
                    # TODO define a placeholder to examine provided value - in this case, showing balance for withdrawal.
                    set_wrapped_value(0)
                    self.assertRaises(InvalidSessionException, sessions[0].withdrawal)
                    set_wrapped_value(-100)
                    self.assertRaises(InvalidSessionException, sessions[1].withdrawal)

                # Test withdrawal amount is positive, but over the balance.
                # - Using second account
                with patch('atm_hardware_driver.select_account_index', get_wrapped_value):
                    set_wrapped_value(1)
                    sessions[2].select_accounts()
                    set_wrapped_value(300)
                    self.assertRaises(InvalidSessionException, sessions[2].withdrawal)"""

                # Test withdrawal amount is positive, proper value.
                # - Using third account
                with patch('atm_hardware_driver.select_account_index', get_wrapped_value):
                    set_wrapped_value(2)
                    sessions[3].select_accounts()
                    set_wrapped_value(30)
                    sessions[3].withdrawal()
                    self.assertEqual(sessions[3]._balance, 170)
        # endregion WITHDRAWAL


if __name__ == '__main__':
    unittest.main(verbosity=1)
