#! python3


from Functions.PreProcessing import PreProcessing
from Functions.MessageSchedule import block_break as BB
from Components.Logic import xor2in as XOR2
from Components.Logic import xor4in as XOR4
from Components.Adder import addmod32 as ADDM32
from Components.Rotator import rotatorright as RTR
from collections import deque


class BLAKE256(PreProcessing):

    def __init__(self):

        PreProcessing.__init__(self, pad_type=1)

        self.__salt0 = "0"*32
        self.__salt1 = "0" * 32
        self.__salt2 = "0" * 32
        self.__salt3 = "0" * 32

        self.__salt = deque([self.__salt0, self.__salt1, self.__salt2, self.__salt3], 4)

        self.__h_constants = self.gather_h_constants()

        self.__pi_constants = self.gather_pi_constants()

        self.__sigs = self.gather_permutations()

        self.__internal_state = None

        self.__block_words = None

        self.__digest = None

    @staticmethod
    def gather_h_constants(constants_path: str=".\\Constants\\h_constants32bit.txt"):

        with open(constants_path, "r") as cfile:

            return tuple(constant.split("\n")[0] for constant in cfile.readlines())

    @staticmethod
    def gather_pi_constants(constants_path: str=".\\Constants\\pi_leading512bit.txt"):

        with open(constants_path, "r") as cfile:

            return tuple(constant.split("\n")[0] for constant in cfile.readlines())

    @staticmethod
    def gather_permutations(perms_path: str=".\\Constants\\permutations0_15.csv"):

        with open(perms_path, "r") as pfile:

            return tuple(tuple(int(c) for c in line.split(",")) for line in pfile.read().split("\n"))

    def subscripts(self, rnd: int, g_i: int):
        return self.__sigs[rnd % 10][2*g_i], self.__sigs[rnd % 10][2*g_i + 1]

    def pi_selector(self, subscript1: int, subscript2: int):
        return self.__pi_constants[subscript1], self.__pi_constants[subscript2]

    def message_box(self, subscript1: int, subscript2: int):
        return self.__block_words[subscript1], self.__block_words[subscript2]

    def input_len_breakdown(self):
        og_len = self.get_input_message_len()
        total_blocks = self.get_total_blocks()
        len_breakdown = deque([], total_blocks)
        for i in range(1, (og_len // 512) + 1):
            len_breakdown.append(512*i)

        if len(len_breakdown) < total_blocks:
            len_breakdown.append(og_len)

        if len(len_breakdown) < total_blocks:
            len_breakdown.append(0)

        return len_breakdown

    def compression_function(self, a, b, c, d, rnd, g_i):

        s2i, s2i_1 = self.subscripts(rnd, g_i)

        u_sig2i, u_sig2i_1 = self.pi_selector(s2i, s2i_1)

        m_sig2i, m_sig2i_1 = self.message_box(s2i, s2i_1)

        a = ADDM32(a, b, "".join((XOR2(m_sig2i[j], u_sig2i_1[j]) for j in range(32))))
        d = RTR("".join((XOR2(d[j], a[j]) for j in range(32))), 16)
        c = ADDM32(c, d)
        b = RTR("".join((XOR2(b[j], c[j]) for j in range(32))), 12)
        a = ADDM32(a, b, "".join((XOR2(m_sig2i_1[j], u_sig2i[j]) for j in range(32))))
        d = RTR("".join((XOR2(d[j], a[j]) for j in range(32))), 8)
        c = ADDM32(c, d)
        b = RTR("".join((XOR2(b[j], c[j]) for j in range(32))), 7)

        return a, b, c, d

    def column_step(self, rnd: int):

        vst = self.__internal_state

        for i in range(4):
            vst[0][i], vst[1][i], vst[2][i], vst[3][i] = self.compression_function(vst[0][i],
                                                                                   vst[1][i],
                                                                                   vst[2][i],
                                                                                   vst[3][i],
                                                                                   rnd,
                                                                                   i)

    def diagonal_step(self, rnd: int):

        vst = self.__internal_state

        for i in range(4):
            vst[0][i], vst[1][(i+1)%4], vst[2][(i+2)%4], vst[3][(i+3)%4] = self.compression_function(vst[0][i],
                                                                                                     vst[1][(i+1)%4],
                                                                                                     vst[2][(i+2)%4],
                                                                                                     vst[3][(i+3)%4],
                                                                                                     rnd,
                                                                                                     i+4)

    def blake256(self, message: str):

        self.__digest = None

        self.set_padded_data(message)
        blocks = self.get_message_blocks()

        counter_lens = self.input_len_breakdown()
        internal_fourths = deque([self.set_internal_4th(cl) for cl in counter_lens], len(counter_lens))

        for b_num in range(len(blocks)):

            self.set_block_words(blocks.popleft())

            self.set_internal_3(self.__digest)
            self.__internal_state.append(internal_fourths.popleft())

            for rnd in range(14):

                self.column_step(rnd)

                self.diagonal_step(rnd)

            self.update_digest(b_num)

        return "".join((f"{int(h_prime, 2):0>8x}" for h_prime in self.__digest))

    def update_digest(self, block_num: int):

        if block_num < 1:
            self.__digest = deque(
                ["".join(
                    (XOR4(self.__h_constants[i][j],
                          self.__salt[i % 4][j],
                          self.__internal_state[0 if i < 4 else 1][i % 4][j],
                          self.__internal_state[2 if i < 4 else 3][i % 4][j]) for j in range(32))
                ) for i in range(8)], 8)

        else:
            self.__digest = deque(
                ["".join(
                    (XOR4(self.__digest[i][j],
                          self.__salt[i % 4][j],
                          self.__internal_state[0 if i < 4 else 1][i % 4][j],
                          self.__internal_state[2 if i < 4 else 3][i % 4][j]) for j in range(32))
                ) for i in range(8)], 8)

    def set_salt(self, salt_0: int=0, salt_1: int=0, salt_2: int=0, salt_3: int=0):
        self.__salt0 = f"{salt_0:0>32b}"
        self.__salt1 = f"{salt_1:0>32b}"
        self.__salt2 = f"{salt_2:0>32b}"
        self.__salt3 = f"{salt_3:0>32b}"

        self.__salt = deque([self.__salt0, self.__salt1, self.__salt2, self.__salt3], 4)

    def set_internal_3(self, chain=None):

        row0 = deque([h for h in self.__h_constants[:4]], 4) if chain is None else \
            deque([chain[c] for c in range(4)], 4)

        row1 = deque([h for h in self.__h_constants[4:]], 4) if chain is None else \
            deque([chain[c] for c in range(4, 8)], 4)

        row2 = deque(["".join((XOR2(self.__salt[i][j], self.__pi_constants[i][j]) for j in range(32))) for i in range(4)], 4)

        self.__internal_state = deque([row0, row1, row2], 4)

    def set_internal_4th(self, len_for_counter: int):
        counter = f"{len_for_counter:0>64b}"

        t = deque([counter[32:], counter[32:], counter[:-32], counter[:-32]], 4)

        return deque(["".join((XOR2(t[i][j], self.__pi_constants[i+4][j]) for j in range(32))) for i in range(4)],
                     4
                     )

    def set_block_words(self, block512: str):
        self.__block_words = deque(BB(block512), 16)

    def get_salt(self):
        return self.__salt

    def get_h_constants(self):
        return self.__h_constants

    def get_pi_constants(self):
        return self.__pi_constants

    def get_permutations(self):
        return self.__sigs

    def get_internal_state(self):
        return self.__internal_state

    def get_digest(self):
        return self.__digest
