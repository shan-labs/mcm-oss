import sys


def parse_input(user_input):
    return user_input.split()


def verify_command(command):
    print(f'mcm-oss: {command}: command not found')
    pass


def prompt(message=None):
    if message:
        print(message)
    return input(">> ").strip()


def input_num(message):
    while True:
        user_input = prompt(message)
        if user_input.isnumeric():
            return user_input
        else:
            print("Invalid value: This value can only be a numeric like `55`")


def interactive():
    ram_max = input_num("How much RAM is on the simulated computer? (bytes)")
    disks_max = input_num("How many hard disks on the simulated computer?")
    print(ram_max, disks_max)
    while True:
        try:
            user_input = prompt()
            print(parse_input(user_input))
        except EOFError:
            print("\nExiting mcm-oss.\nHave a nice day!")
            sys.exit()
        except KeyboardInterrupt:
            print()
            pass
