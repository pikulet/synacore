from .status import Status
from .opcodes import Opcode
from core.storage import Memory, Registers, Stack
from core.io.io import IO

class Synacore:

    def __init__(self, initial_memory: bytearray):
        self.__memory = Memory(initial_memory)
        self.__io = IO()
        self.__registers = Registers()
        # self.__stack = Stack()
        self.__instruction_ptr = 0

    def run(self):
        while True:
            result = self.__run_next_instruction()
            match result:
                case Status.OK:
                    continue
                case Status.TERMINATED:
                    continue
                    #self.__output("success")
                    #return
                case Status.ERROR:
                    self.__output("error_encountered")
                    return

    def __run_next_instruction(self) -> Status:
        opcode = self.__read_next_in_memory()

        match Opcode(opcode):
            case Opcode.HALT:
                return self.__execute_halt()
            case Opcode.OUT:
                return self.__execute_out()
            case Opcode.NOOP:
                return self.__execute_noop()

        return Status.ERROR

    def __read_next_in_memory(self) -> int:
        result = self.__memory.get(self.__instruction_ptr)
        self.__instruction_ptr += 1
        return result

    def __output(self, s):
        self.__io.output(s)

    def __execute_halt(self) -> Status:
        return Status.TERMINATED

    def __execute_out(self) -> Status:
        a = self.__read_next_in_memory()
        result = chr(a)
        self.__output(result)
        return Status.OK

    def __execute_noop(self) -> Status:
        return Status.OK
