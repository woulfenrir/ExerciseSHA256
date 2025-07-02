#! python3


from collections import deque
from os import getcwd as gc
from os.path import join as pj
from Components.Adder import addmod32
from Functions.TempOne import tw1 as T1
from Functions.TempTwo import tw2 as T2


def compress(word_schedule: iter, initial_hash: iter):

    working_hash = deque(initial_hash, len(initial_hash))

    with open(pj(gc(), "Constants\\k_constants32bit.txt"), "r+") as kcfile:

        i = 0
        kt = kcfile.readline().split("\n")[0]
        while len(kt) > 0:

            tw1 = T1(working_hash[-4],
                     working_hash[-3],
                     working_hash[-2],
                     working_hash[-1],
                     kt,
                     word_schedule[i])

            tw2 = T2(working_hash[-8],
                     working_hash[-7],
                     working_hash[-6])

            working_hash.appendleft(addmod32(tw1, tw2))
            working_hash[-4] = addmod32(working_hash[-4], tw1)

            i += 1
            kt = kcfile.readline().split("\n")[0]

    return [addmod32(working_hash[j], initial_hash[j]) for j in range(8)]
