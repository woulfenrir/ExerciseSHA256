#! python3


from Components.Adder import addmod32
from Components.Choice import choice as Ch
from Functions.bigsigmas import bigsigma1 as BS1


def bigchoice(e, f, g):

    return "".join((Ch(g[i], f[i], choicebit=e[i]) for i in range(32)))


def tw1(e, f, g, h, k, w):

    bs1_e = BS1(e)
    ch_efg = bigchoice(e, f, g)

    return addmod32(bs1_e, ch_efg, h, k, w)
