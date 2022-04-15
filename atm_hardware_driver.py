# Template of ATM hardware driver


def get_cash_bin() -> int:
    # TODO codes here - returns how much of cash is in ATM.
    raise NotImplementedError()


def get_card_number():
    # TODO codes here - waits for the card and return card number to the controller.
    # card_number = ''
    # return card_number
    raise NotImplementedError()


def get_pin():
    # TODO codes here - waits for the pin input and return it to the controller.
    # pin = ''
    # return pin
    raise NotImplementedError()


def select_account_index(accounts):
    # TODO codes here - displays given account numbers, and waits for user selection.
    raise NotImplementedError()


def select_main_menu() -> int:
    # TODO codes here - shows actions a user can do, and waits for the decision.
    raise NotImplementedError()


def show_balance(balance) -> bool:
    # TODO codes here - displays the balance of the current account, and returns to finish or go back to main menu.
    raise NotImplementedError()


def deposit() -> int:
    # TODO codes here - performs deposit, and returns how much of money has been charged.
    raise NotImplementedError()


def withdrawal_amount(balance) -> int:
    # TODO codes here - shows balance, and gets input the amount of money to withdraw.
    raise NotImplementedError()


def withdraw(amount):
    # TODO codes here - performs withdrawal.
    raise NotImplementedError()


def finalize_and_return_card():
    # TODO codes here - ATM will do mechanical stuffs after the finish of transaction and return the inserted card.
    raise NotImplementedError()


