import sys


def pipeline(f):
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

        if result:
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
                print("process")
                return
        if command_length == 2:
            if command[0] == 'S' and command[1] in ["r", "i", "m"]:
                print("show")
                return
            if command[0] in ["A", "Ar", "d", "D"] and command[1].isnumeric():
                print("num arg")
                return
    print(f'mcm-oss: {" ".join(command)}: command not found')
    return False


def input_num_raw(message):
    while True:
        user_input = prompt(message)
        if user_input.isnumeric():
            return user_input
        print("Invalid value: This value can only be a numeric like `55`")


def input_num(message):
    return pipeline(lambda: input_num_raw(message))


def program(ram_max, disks_max):
    user_input = prompt()
    parsed_input = parse_input(user_input)
    context = command_function(parsed_input)
    print(context)
    pass


def interactive():
    ram_max = input_num("How much RAM is on the simulated computer? (bytes)")
    disks_max = input_num("How many hard disks on the simulated computer?")
    pipeline(lambda: program(ram_max, disks_max))
