from audioop import add
from sys import byteorder
from .const import *

class Memory:
    
    def __init__(self, initial_memory: bytearray):
        # memory
        self.__data = initial_memory
        num_indexable_bytes = 2**MEM_ADDRESS_SPACE * NUM_BYTES_PER_WORD
        extension_length = num_indexable_bytes - len(self.__data)
        self.__data.extend(bytearray(extension_length))

    def get(self, address: int) -> int:
        byte_data = self.__data[NUM_BYTES_PER_WORD * address: NUM_BYTES_PER_WORD * (address + 1)]
        return int.from_bytes(byte_data, "little", signed="false")