"""
Khinshan Khan - cli.py.

This module contains all command line interaction with user.
"""
import sys


def input_monad(f):
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


def parse_input(user_input):
    return user_input.split()


def prompt(message=None):
    if message:
        print(message)
    return input(">> ").strip()


def command_function(command):
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


def input_num_raw(message):
    while True:
        user_input = prompt(message)
        if user_input.isnumeric():
            return user_input
        print("Invalid value: This value can only be a numeric like `55`")


def input_num(message):
    return pipeline(lambda: input_num_raw(message))


def initialize():
    ram_max = input_num("How much RAM is on the simulated computer? (bytes)")
    disks_max = input_num("How many hard disks on the simulated computer?")
    return (ram_max, disks_max)


def interactive(ram_max, disks_max):
    user_input = pipeline(prompt)
    parsed_input = parse_input(user_input)
    context, arguments = command_function(parsed_input)
    return (context, arguments)
