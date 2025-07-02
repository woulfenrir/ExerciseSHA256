#! python3


def xor2in(bitone: str, bittwo: str):

    return str((bitone+bittwo).count("1") % 2)


def xor3in(bitone: str, bittwo: str, bitthree: str):

    return str((bitone+bittwo+bitthree).count("1") % 2)


def xor4in(bitone: str, bittwo: str, bitthree: str, bitfour: str):

    return str((bitone+bittwo+bitthree+bitfour).count("1") % 2)
