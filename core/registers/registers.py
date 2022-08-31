from core.common.const import NUM_BYTES_PER_WORD
from pprint import pprint


class Registers:
    def __init__(self, num_registers: int):
        self.__registers = [bytearray(NUM_BYTES_PER_WORD)] * num_registers

    def get(self, index: int) -> bytearray:
        return self.__registers[index]

    def set(self, index: int, value: bytearray):
        self.__registers[index] = value

    def inspect(self):
        pprint(self.__registers)
