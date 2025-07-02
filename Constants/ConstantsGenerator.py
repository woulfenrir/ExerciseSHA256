#! python3


from Constants.PrimesGenerator import generate_primes
from gmpy2 import mpfr, floor, get_context


class CryptoConstantGenerator:

    get_context().precision = 100

    def __init__(self, bits_64=False, hex_dec=False):

        self.__word_len = 64 if bits_64 else 32
        self.__format_spec = f"{{:0>{self.__word_len//4}x}}" if hex_dec else f"{{:0>{self.__word_len}b}}"

    @staticmethod
    def cubed_root_frac(num: int):

        cubed_root = mpfr(num) ** (1 / mpfr(3))

        return cubed_root - floor(cubed_root)

    @staticmethod
    def square_root_frac(num: int):

        square_root = mpfr(num) ** (1 / mpfr(2))

        return square_root - floor(square_root)

    @staticmethod
    def int2bin(dec_num: int):
        base = mpfr(2)
        quotient = mpfr(dec_num)
        b_string = ""

        while int(quotient) > 0:
            b_string = str(int(quotient % base)) + b_string
            quotient = floor(quotient / base)

        return b_string

    @staticmethod
    def binary_add(bit_string1, bit_string2):
        string_len = max(len(bit_string1), len(bit_string2))
        bit_string1 = bit_string1.zfill(string_len)
        bit_string2 = bit_string2.zfill(string_len)

        result = ""
        carry = "0"

        for i in range(-1, -(string_len + 1), -1):
            chain = carry + bit_string1[i] + bit_string2[i]
            one_count = chain.count("1")
            result = str(one_count % 2) + result

            carry = "1" if one_count > 1 else "0"

        result = carry + result if carry.count("1") > 0 else result

        return result

    def generate_k(self):

        return (self.__format_spec.format(int(self.cubed_root_frac(prime) * (2 ** self.__word_len)))
                for prime in generate_primes(total=64))

    def generate_h(self):

        return (self.__format_spec.format(int(self.square_root_frac(prime) * (2 ** self.__word_len)))
                for prime in generate_primes(total=8))

    def generate_c(self):

        get_context().precision = 10000

    def set_format(self, bits_64=False, hex_dec=False):

        self.__word_len = 64 if bits_64 else 32
        self.__format_spec = f"{{:0>{self.__word_len//4}x}}" if hex_dec else f"{{:0>{self.__word_len}b}}"
