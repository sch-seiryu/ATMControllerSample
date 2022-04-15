import uuid
from functools import wraps

import atm_hardware_driver as ahd
from bank_api import request_authorization, request_accounts, get_balance, update_balance


# region User Defined Exceptions
class InvalidSessionException(BaseException):

    def __init__(self, msg=''):
        super(InvalidSessionException, self).__init__(msg or "Invalid Session. Session Has Been Corrupted.")


class InvalidPinNumberException(InvalidSessionException):
    
    def __init__(self):
        super(InvalidPinNumberException, self).__init__("Invalid Pin Number.")


class UserInterruptionException(InvalidSessionException):

    def __init__(self):
        super(UserInterruptionException, self).__init__("User terminated session.")
# endregion User Defined Exceptions


class Session:

    def __init__(self):
        """ATM Controller works based on a session, including each given stage; all 4 stages.
        This 'Session' class only includes required functionalities, yet not a stand alone program.
        """
        self._uuid = uuid.uuid4()
        # Unique identifier for each session.(random)
        self._card_number = ''
        # Current card number.

        self._status = 0  # 0: initial state, 1: card inserted, 2: authorized, 3: account selected, 4: expired
        self._auth = False
        self._account = ''
        self._balance = 0
        self._alive = True

    @property
    def auth(self) -> bool:
        """

        :return: bool True if this session has got an auth over bank API.
        """
        return self._auth

    @property
    def status(self) -> int:
        """

        :return: int status code; 0: initial state, 1: card inserted, 2: authorized, 3: account selected, 4: expired
        """
        return self._status

    @property
    def alive(self) -> bool:
        """

        :return: bool True if session is not expired.
        """
        return self._alive

    def _self_destruction_on_failure_or_termination(func):
        """Must be called after any kind of ends of a session work flow, to identify the session is expired.
        And finally, an inserted card will be returned. -> Changed into working as a decorator.

        :return:
        """
        @wraps(func)
        def wrapped_func(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except InvalidSessionException:
                # set all codes for expiration
                self._status = 4
                self._alive = False

                # make machine return the card and allow cleanups
                ahd.finalize_and_return_card()

                raise
        return wrapped_func

    @_self_destruction_on_failure_or_termination
    def read_card(self):
        # When the card number is already set(inserted).
        if self._card_number:
            # self._self_destruct()
            raise InvalidSessionException()  # Session finalization failure or hardware error.

        self._card_number = ahd.get_card_number()

        # update session status
        self._status = 1

    @_self_destruction_on_failure_or_termination
    def authorize(self, pin):
        # unable to authorize multiple times
        if self._auth or self._status != 1:
            # self._self_destruct()
            raise InvalidSessionException()

        # request authorization to bank API
        if request_authorization(self._card_number, pin):
            self._auth = True

            # update session status
            self._status = 2
            return

        # Authorization denied
        # self._self_destruct()
        raise InvalidPinNumberException()

    @_self_destruction_on_failure_or_termination
    def select_accounts(self):
        # authorization must be done first
        if self._auth is False or self._status != 2:
            # self._self_destruct()
            raise InvalidSessionException()

        # request account list to bank API
        accounts = request_accounts(self._card_number)

        # make user select which account to use - only index returns from input system.
        try:
            selected_index = ahd.select_account_index(accounts)
            if selected_index < 0:
                raise IndexError()
            self._account = accounts[selected_index]

            # request the balance of the account to bank API
            self._balance = get_balance(self._account)
        except IndexError:
            # self._self_destruct()
            raise InvalidSessionException("Failed to select an account.")

        # update session status
        self._status = 3

    @_self_destruction_on_failure_or_termination
    def show_balance(self):
        if ahd.show_balance(self._balance) is False:
            # self._self_destruct()
            raise InvalidSessionException('Failed to show balance.')

    @_self_destruction_on_failure_or_termination
    def deposit(self):
        # check integrity by status code
        if self._status != 3:
            # self._self_destruct()
            raise InvalidSessionException()

        # let machine deposit the money. When nothing is input, the amount is 0$.
        amount = ahd.deposit()
        if amount >= 0:
            # update balance and send it through bank API
            self._balance += amount
            update_balance(self._account, self._balance)
        else:
            raise InvalidSessionException('Unable to deposit money.')

        # show balance screen as a result
        self.show_balance()

    @_self_destruction_on_failure_or_termination
    def withdrawal(self):
        # check integrity by status code
        if self._status != 3:
            # self._self_destruct()
            raise InvalidSessionException()

        # let user input the amount of money to withdraw.(until proper value is given) '-1$' to abort.
        # TODO - the machine driver is must implemented to return a proper value for exit condition as written above.
        while True:
            amount = ahd.withdrawal_amount(self._balance)
            if 0 < amount <= self._balance:
                # update balance and send it through bank API
                self._balance -= amount
                update_balance(self._account, self._balance)
                break
            elif amount < 0:
                break
            # TODO - (make machine) show proper messages for each exception.

        # show balance screen as a result
        self.show_balance()

    @_self_destruction_on_failure_or_termination
    def select_menu(self):
        # check integrity by status code
        if self._status != 3:
            # self._self_destruct()
            raise InvalidSessionException()

        task = ahd.select_main_menu()
        if task == 0:
            self.show_balance()
        elif task == 1:
            self.deposit()
        elif task == 2:
            self.withdrawal()

        # Invalid menu
        # self._self_destruct()
        raise InvalidSessionException("Failed to select menu.")
