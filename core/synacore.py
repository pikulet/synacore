from .exception import SynacoreException
from .opcodes import Opcode
from core.storage import Storage, InvalidAddressException
from core.io import IO

class Synacore:

    def __init__(self, initial_memory: bytearray):
        self.__storage = Storage(initial_memory)
        self.__io = IO()
        # self.__stack = Stack()
        self.__instruction_ptr = 0

    def run(self):
        while True:
            try:
                exit = self.__run_next_instruction()
                if exit:
                    return
            except SynacoreException as e:
                self.__io.output(repr(e))
                return

    def __run_next_instruction(self):

        try: 
            opcode = self.__read_next_in_memory()

            match Opcode(opcode):
                case Opcode.HALT:
                    return self.__execute_halt()
                case Opcode.JMP:
                    return self.__execute_jmp()
                case Opcode.JT:
                    return self.__execute_jt()
                case Opcode.OUT:
                    return self.__execute_out()
                case Opcode.NOOP:
                    return self.__execute_noop()
            
            raise OpcodeNotSupportedException(Opcode(opcode))

        except ValueError:
            raise InvalidOpcodeException(opcode)

    def __read_next_in_memory(self) -> int:
        result = self.__storage.get(self.__instruction_ptr)
        self.__instruction_ptr += 1
        return result

    def __read_value_at_next_in_memory(self) -> int:
        address = self.__read_next_in_memory()
        return self.__storage.get(address)

    def __output(self, s):
        self.__io.output(s)

    def __execute_halt(self) -> bool:
        return True

    def __execute_jmp(self):
        a = self.__read_value_at_next_in_memory()
        self.__instruction_ptr = a

    def __execute_jt(self):
        a = self.__read_value_at_next_in_memory()
        b = self.__read_value_at_next_in_memory()

        if a != 0:
            self.__instruction_ptr = b

    def __execute_out(self):
        a = self.__read_next_in_memory()
        result = chr(a)
        self.__output(result)

    def __execute_noop(self):
        pass

class OpcodeNotSupportedException(SynacoreException):

    def __init__(self, opcode: Opcode):
        super().__init__(opcode)

class InvalidOpcodeException(SynacoreException):

    def __init__(self, opcode: Opcode):
        super().__init__(opcode)