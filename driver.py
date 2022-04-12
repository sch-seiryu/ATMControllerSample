# WARNING - this code is currently out of scope.

from atm_controller import Session


__is_alive = True


if __name__ == '__main__':

    # TODO start first session(NOTE - instantiated while import)

    while __is_alive:
        # Making an exit point to stop program.
        command = input('Press enter to start next session. Or input \'q\' to terminate.')
        command = command.strip().casefold()
        if command == 'q':
            break

        # continue to next session
        # restart_session()
