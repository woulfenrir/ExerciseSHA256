#! python3


from Components.Rotator import rotatorright as ROTR
from Components.Logic import xor3in as XOR3


def bigsigma0(thirty2bit: str):

    rotr2 = ROTR(thirty2bit, 2)
    rotr13 = ROTR(thirty2bit, 13)
    rotr22 = ROTR(thirty2bit, 22)

    return "".join((XOR3(rotr2[i], rotr13[i], rotr22[i]) for i in range(32)))


def bigsigma1(thirty2bit: str):

    rotr6 = ROTR(thirty2bit, 6)
    rotr11 = ROTR(thirty2bit, 11)
    rotr25 = ROTR(thirty2bit, 25)

    return "".join((XOR3(rotr6[i], rotr11[i], rotr25[i]) for i in range(32)))
