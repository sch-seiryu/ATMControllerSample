import uuid
import gc

from atm_hardware_driver import get_card_number
# import atm_hardware_driver


# region User Defined Exceptions
class InvalidSessionException(BaseException):

    def __init__(self, msg=''):
        super(InvalidSessionException, self).__init__(msg or "Invalid Session. Session Has Been Corrupted.")


class InvalidPinNumberException(InvalidSessionException):
    
    def __init__(self):
        super(InvalidPinNumberException, self).__init__("Invalid Pin Number.")
# endregion User Defined Exceptions


# region Authorization
class Session:

    def __init__(self):
        """
        """
        self._uuid = uuid.uuid4()
        # Unique identifier for each session.(random)
        self._card_number = ''
        # Current card number.

        # region UNDER_CONSIDERATION
        self._status = 0
        self._auth = False
        self._accounts = {}
        self._alive = True
        # endregion UNDER_CONSIDERATION

    def terminate_session(self):
        self._alive = False
        pass

    def read_card(self):
        # TODO integrate with hardware driver
        # When the card number is already set(inserted).
        if self._card_number:
            raise InvalidSessionException()  # Session finalization failure or hardware error.

        self._card_number = get_card_number()
        # self._card_number = atm_hardware_driver.get_card_number()

    # def set_card_number(self, card_number):
    #     # When the card number is already set(inserted).
    #     if self._card_number:
    #         raise InvalidSessionException()  # Session finalization failure or hardware error.
    #
    #     self._card_number = card_number

    def _request_authorization(self, pin_number):
        # TODO integrate with core banking system
        return False

    def authorize(self, pin_number):
        if self._request_authorization(pin_number):
            raise InvalidPinNumberException()

    def select_accounts(self):
        if self._auth is False:
            raise InvalidSessionException()
        pass


__current_session: Session = Session()
# is_card_inserted = False
#
#
# def wait_for_card_insertion():
#     while ~is_card_inserted:
#         pass


def run_session():
    pass


def restart_session():
    """

    :return:
    """
    global __current_session

    # clear last session
    old_session = __current_session
    try:
        del [[old_session], []]
        gc.collect()
    except NameError:
        pass

    # start new session
    __current_session = Session()


def check_pin():
    pass


# endregion Authorization


