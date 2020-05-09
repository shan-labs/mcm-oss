"""
Khinshan Khan - cli.py.

This module contains all command line interaction with user.
"""
import sys


def prompt(message):
    """Print optional message and wait for user input."""
    if message:
        print(message)
    return input(">> ").strip()


def input_monad(message):
    """Listen for user events and acts accordingly, or else returns given input value ."""
    result = None
    while True:
        try:
            result = prompt(message)
        except EOFError:
            print("\nExiting mcm-oss.\nHave a nice day!")
            sys.exit()
        except KeyboardInterrupt:
            print()
            continue

        if result is not None:
            return result


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
    return (False, " ".join(command))


def interactive():
    """Get the next command user enters and pass it up to main."""
    user_input = input_monad(None)
    parsed_input = user_input.split()
    context, arguments = verify_command(parsed_input)
    return (context, arguments)


def input_num(message):
    """Get an input which is ensured to be a numeric."""
    while True:
        user_input = input_monad(message)
        if user_input.isnumeric():
            return int(user_input)
        print("Invalid value: This value can only be a numeric like `55`")


def initialize():
    """Get necessary values for simulation."""
    ram_size = input_num("How much RAM is on the simulated computer? (bytes)")
    disks_max = input_num("How many hard disks on the simulated computer?")
    return (ram_size, disks_max)
