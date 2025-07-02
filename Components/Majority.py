#! python3


def majority(*bits):

    return max((bits.count("1"), "1"), (bits.count("0"), "0"))[1]
