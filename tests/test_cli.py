from mcm_oss.cli import (
    verify_command
)


def test_verify_command():
    assert verify_command([]) == (False, '')
    assert verify_command(["55"]) == (False, '55')

    assert verify_command(["A", "5"]) == ("A", "5")
    assert verify_command(["Ar", "5"]) == ("Ar", "5")

    assert verify_command(["A", "i"]) == (False, 'A i')
    assert verify_command(["Ar", "i"]) == (False, 'Ar i')
    assert verify_command(["AR", "i"]) == (False, 'AR i')
    assert verify_command(["A", "5i"]) == (False, 'A 5i')
    assert verify_command(["Ar", "i5"]) == (False, 'Ar i5')

    assert verify_command(["Q"]) == ("Q", None)
    assert verify_command(["t"]) == ("t", None)
    assert verify_command(["Q", "i"]) == (False, 'Q i')
    assert verify_command(["t", "i"]) == (False, 't i')

    # similar to A and Ar tests
    assert verify_command(["d", "5"]) == ("d", "5")
    assert verify_command(["D", "5"]) == ("D", "5")

    assert verify_command(["S", "r"]) == ('S', 'r')
    assert verify_command(["S", "i"]) == ('S', 'i')
    assert verify_command(["S", "m"]) == ('S', 'm')

    assert verify_command(["S"]) == (False, 'S')
    assert verify_command(["S", "j"]) == (False, 'S j')
