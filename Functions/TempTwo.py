#! python3


from Components.Adder import addmod32
from Components.Majority import majority as Maj
from Functions.bigsigmas import bigsigma0 as BS0


def bigmajority(a, b, c):

    return "".join((Maj(a[i], b[i], c[i]) for i in range(32)))


def tw2(a, b, c):

    bs0_a = BS0(a)
    maj_abc = bigmajority(a, b, c)

    return addmod32(bs0_a, maj_abc)
