#! python3


from Components.Shifter import shifterright as SHR
from Components.Rotator import rotatorright as ROTR
from Components.Logic import xor3in as XOR3


def lilsigma0(thirty2bit: str):

    rotr7 = ROTR(thirty2bit, 7)
    rotr18 = ROTR(thirty2bit, 18)
    shr3 = SHR(thirty2bit, 3)

    return "".join((XOR3(rotr7[i], rotr18[i], shr3[i]) for i in range(len(thirty2bit))))


def lilsigma1(thirty2bit: str):

    rotr17 = ROTR(thirty2bit, 17)
    rotr19 = ROTR(thirty2bit, 19)
    shr10 = SHR(thirty2bit, 10)

    return "".join((XOR3(rotr17[i], rotr19[i], shr10[i]) for i in range(len(thirty2bit))))
