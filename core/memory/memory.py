from audioop import add
from sys import byteorder
from core.common.const import *


class Memory:
    def __init__(self, initial_memory: bytearray):
        # memory
        self.__data = initial_memory
        num_indexable_bytes = 2**MEM_ADDRESS_SPACE * NUM_BYTES_PER_WORD
        extension_length = num_indexable_bytes - len(self.__data)
        self.__data.extend(bytearray(extension_length))

    def get(self, address: int) -> bytearray:
        return self.__data[
            NUM_BYTES_PER_WORD * address : NUM_BYTES_PER_WORD * (address + 1)
        ]

    def set(self, address: int, value: bytearray) -> bytearray:
        start_pos = NUM_BYTES_PER_WORD * address
        for index in range(NUM_BYTES_PER_WORD):
            self.__data[start_pos + index] = value[index]
