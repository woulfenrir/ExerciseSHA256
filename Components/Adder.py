#! python3


def addmod32(*thirty2bitstrings):

    return f"{sum((int(thirty2bitstring, 2) for thirty2bitstring in thirty2bitstrings)) % (2**32):0>32b}"
