# Template of banking API


# class BankAPI:
#
#     def __init__(self):
#         pass
#         # 음... 굳이 이렇게 객체 만들어서 하는것 보다 그냥 json 형태로 받는게 낫지 않나.
#
#     def request_authorization(self, card_number, pin):
#         return
#
#     def request_accounts(self):
#         pass


def request_authorization(card_number, pin) -> bool:
    """Examine given pair of card number and PIN are correct or not.

    :param card_number:
    :param pin:
    :return:
    """
    # TODO codes here - wait for the card and return card number to the controller
    # return False
    raise NotImplementedError()


def request_accounts(card_number) -> list:
    """Get bank accounts from given card number.
    TODO integrate authentication feature for safe transaction

    :param card_number:
    :return:
    """
    # TODO codes here - wait for the card and return card number to the controller
    # return []
    raise NotImplementedError()


def get_balance(account) -> int:
    """Get balance of a specific bank account.
    TODO integrate authentication feature for safe transaction

    :param account:
    :return:
    """
    # return 0
    raise NotImplementedError()


def update_balance(account, balance):
    """Update balance of an account after deposit or withdrawal.
    TODO integrate authentication feature for safe transaction

    :param account:
    :param balance:
    :return:
    """
    # TODO codes here - wait for the card and return card number to the controller
    raise NotImplementedError()
