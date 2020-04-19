import sys


def interactive():
    while True:
        try:
            user_input = input(">> ")
            print(user_input)
        except EOFError:
            print("\nExiting mcm-oss.\nHave a nice day!")
            sys.exit()
        except KeyboardInterrupt:
            print()
            pass
