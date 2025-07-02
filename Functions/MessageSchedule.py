#! python3


from Components.Adder import addmod32
from Functions.lilsigmas import lilsigma0 as lils0
from Functions.lilsigmas import lilsigma1 as lils1


def block_break(block512: str):

    return [block512[i:32+i] for i in range(0, 512, 32)]


def prepare_ms(block512: str):

    words = block_break(block512)

    for w in range(16, 64):

        wt_16 = words[-16]
        ls0_wt_15 = lils0(words[-15])
        wt_7 = words[-7]
        ls1_wt_2 = lils1(words[-2])

        words.append(addmod32(wt_16, ls0_wt_15, wt_7, ls1_wt_2))

    return words
