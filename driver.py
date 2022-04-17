from atm_controller import Session


if __name__ == '__main__':

    def create_session() -> Session:
        return Session()

    __is_alive = True
    __session = create_session()
    while __is_alive:
        # Making an exit point to stop program.
        command = input('Press enter to start next session. Or input \'q\' to terminate.')
        command = command.strip().casefold()
        if command == 'q':
            break

        # Simulating session
        # TODO hardware driver should be replaced with proper one to simulate controller with console. Keep remaining out of scope.
