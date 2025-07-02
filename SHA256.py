#! python3

import os
from collections import deque
from Functions.PreProcessing import PreProcessing
from Functions.MessageSchedule import prepare_ms as PMS
from Functions.Compression import compress as COMP


def initialize_hash():

    with open(os.path.join(os.getcwd(), "Constants\\h_constants32bit.txt"), "r+") as hcfile:

        return [word.split("\n")[0] for word in hcfile.readlines()]


def sha256(message: str):

    prepro = PreProcessing()

    block_stream, total_blocks, message_length = prepro.data_padding(message, 0)

    message_schedule = deque([], total_blocks)

    m = 0
    while m < total_blocks:

        message_schedule.append(PMS(block_stream[512*m:512*(m+1)]))
        m += 1

    resulting_hash = COMP(message_schedule.popleft(), initialize_hash())

    while len(message_schedule) > 0:

        resulting_hash = COMP(message_schedule.popleft(), resulting_hash)

    return "".join(("0"*(8-len(f"{int(hash_piece, 2):x}")) +
                    f"{int(hash_piece, 2):x}" for hash_piece in resulting_hash))

for c in "abcdefghijklmnopqrstuvwxyz":
    print(sha256(c))
