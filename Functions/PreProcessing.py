#! python3

from math import sin, pi
from collections import deque


class PreProcessing:
    """
    This object class holds data attribute values for messages meant to be hashed using either
    SHA256 or BLAKE256.
    """

    def __init__(self, pad_type: int=0):
        """
        Set 'pad_type' to '0' for SHA256 padding and '1' for BLAKE256 padding.
        :param pad_type: '0' -> SHA256 Padding
                            '1' -> BLAKE256 Padding
        """

        self.__pad_type = pad_type
        self.__input_message = ""
        self.__input_message_bin = ""
        self.__padded_message = ""
        self.__total_blocks = 0
        self.__input_message_len = 0
        self.__message_blocks = None

    @staticmethod
    def generate_bins_from_str(message: str):
        return (f"{ord(c):0>8b}" for c in message)

    def data_padding(self, message: str, pad_type: int=0):
        """
        Takes an input of type 'str' and returns a bit string of a length size that
        is a multiple of 512 according to either SHA256 or BLAKE pre-processing standards,
        and determined by 'pad_type' chosen to be either 0 or 1.

        :param message: Any string of bit length 0 < len < 2**64 -1

        :param pad_type: Choose '0' for SHA256 padding or '1' for BLAKE padding.

        :return: Tuple containing the binary representation of the input message
                    padded with bits corresponding to either SHA256 or BLAKE style
                    of padding, the total number of 512-bit blocks, and the bit length
                    of the original input message.
        """

        if not 0 <= pad_type < 2:
            raise ValueError("Input 'pad_type' must be '0' or '1'")

        congruent_len = (2+(~pad_type))*447 + pad_type*446

        self.__input_message_bin = "".join(self.generate_bins_from_str(message))

        input_msg_len = len(self.__input_message_bin)

        zpad_factor = congruent_len - (input_msg_len % 512)
        zpad_factor += 512*(round(sin(pi - (2**(zpad_factor//abs(zpad_factor)))*pi)))

        padded_message = self.__input_message_bin + "1" + "0"*zpad_factor + "1"*pad_type + f"{input_msg_len:0>64b}"

        total_blocks = len(padded_message) // 512

        return padded_message, total_blocks, input_msg_len

    def set_pad_type(self, pad_type: int=0):
        self.__pad_type = pad_type

    def set_padded_data(self, message: str):

        self.__input_message = message

        self.__padded_message,\
            self.__total_blocks,\
            self.__input_message_len = self.data_padding(message=message, pad_type=self.__pad_type)

        self.__message_blocks = deque([self.__padded_message[i*512:(i+1)*512] for i in range(self.__total_blocks)],
                                      self.__total_blocks
                                      )

    def get_padded_message(self):
        return self.__padded_message

    def get_total_blocks(self):
        return self.__total_blocks

    def get_input_message_len(self):
        return self.__input_message_len

    def get_input_message(self):
        return self.__input_message

    def get_input_message_bin(self):
        return self.__input_message_bin

    def get_message_blocks(self):
        return self.__message_blocks
