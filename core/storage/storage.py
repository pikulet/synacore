from core.exception import SynacoreException
from core.storage.const import REGISER_MAX, REGISTER_MIN
from .memory import Memory
from .registers import Registers

class Storage:

    def __init__(self, initial_memory: bytearray):
        self.__memory = Memory(initial_memory)
        self.__registers = Registers()

    def get(self, address: int) -> int:
        if address < REGISTER_MIN:
            return self.__memory.get(address)
        elif address <= REGISER_MAX:
            return self.__registers.get(address)
        
        raise InvalidAddressException(address)

class InvalidAddressException(SynacoreException):
    def __init__(self, address: int):
        super().__init__(address)