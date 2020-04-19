"""
Khinshan Khan - cli.py.

This module contains all command line interaction with user.
"""
import sys


def input_monad(f):
    """Listen for user events and acts accordingly, or else returns value of given function."""
    result = None
    while True:
        try:
            result = f()
        except EOFError:
            print("\nExiting mcm-oss.\nHave a nice day!")
            sys.exit()
        except KeyboardInterrupt:
            print()
            continue

        if result is not None:
            return result


def prompt(message=None):
    """Print optional message and wait for user input."""
    if message:
        print(message)
    return input(">> ").strip()


def verify_command(command):
    """Verify a given command is legal."""
    command_length = len(command)
    if command_length > 0:
        if command_length == 1:
            if command[0] in ["Q", "t"]:
                return (command[0], None)
        if command_length == 2:
            if ((command[0] == 'S' and command[1] in ["r", "i", "m"])
                    or (command[0] in ["A", "Ar", "d", "D"] and command[1].isnumeric())):
                return (command[0], command[1])
    return (False, command)


def interactive(ram_max, disks_max):
    """Get the next command user enters and pass it up to main."""
    user_input = input_monad(prompt)
    parsed_input = user_input.split()
    context, arguments = verify_command(parsed_input)
    return (context, arguments)


def input_num(message):
    """Get an input which is ensured to be a numeric."""
    def input_num_raw(message):
        """Body function of `input_num`, to ensure encapsulation in `input_monad`."""
        while True:
            user_input = prompt(message)
            if user_input.isnumeric():
                return user_input
            print("Invalid value: This value can only be a numeric like `55`")
    return input_monad(lambda: input_num_raw(message))


def initialize():
    """Get necessary values for simulation."""
    ram_max = input_num("How much RAM is on the simulated computer? (bytes)")
    disks_max = input_num("How many hard disks on the simulated computer?")
    return (ram_max, disks_max)
