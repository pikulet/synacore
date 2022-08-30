from core.common.const import *
from core.common.exception import SynacoreException
from core.opcodes import Opcode
from core.memory import Memory
from core.registers import Registers
from core.io import IO


class Synacore:
    def __init__(self, initial_memory: bytearray):
        self.__memory = Memory(initial_memory)
        self.__registers = Registers(REGISTER_MAX - REGISTER_MIN + 1)
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
                case Opcode.JF:
                    return self.__execute_jf()
                case Opcode.OUT:
                    return self.__execute_out()
                case Opcode.NOOP:
                    return self.__execute_noop()

            raise OpcodeNotSupportedException(Opcode(opcode))

        except ValueError:
            raise InvalidOpcodeException(opcode)

    def __read_next_in_memory(self) -> int:
        result = self.__memory.get(self.__instruction_ptr)
        self.__instruction_ptr += 1
        return result

    def __evaluate_next_in_memory(self) -> int:
        value = self.__read_next_in_memory()
        if value < MODULO_BASE:
            return value
        elif value <= REGISTER_MAX:
            return self.__registers.get(value - MODULO_BASE)
        else:
            raise InvalidValueException(value)

    def __output(self, s):
        self.__io.output(s)

    def __execute_halt(self) -> bool:
        """
        halt: 0
        stop execution and terminate the program
        """
        return True

    def __execute_jmp(self):
        """
        jmp: 6 a
        jump to <a>
        """
        a = self.__evaluate_next_in_memory()
        self.__instruction_ptr = a

    def __execute_jt(self):
        """
        jt: 7 a b
        if <a> is nonzero, jump to <b>
        """
        a = self.__evaluate_next_in_memory()
        b = self.__evaluate_next_in_memory()

        if a != 0:
            self.__instruction_ptr = b

    def __execute_jf(self):
        """
        jf: 8 a b
        if <a> is zero, jump to <b>
        """
        a = self.__evaluate_next_in_memory()
        b = self.__evaluate_next_in_memory()

        if a == 0:
            self.__instruction_ptr = b

    def __execute_out(self):
        """
        out: 19 a
        write the character represented by ascii code <a> to the terminal
        """
        a = self.__evaluate_next_in_memory()
        result = chr(a)
        self.__output(result)

    def __execute_in(self):
        """
        in: 20 a
        read a character from the terminal and write its ascii code to <a>; it can be assumed that once input starts, it will continue until a newline is encountered; this means that you can safely read whole lines from the keyboard and trust that they will be fully read
        """
        pass

    def __execute_noop(self):
        """
        noop: 21
        no operation
        """
        pass


class OpcodeNotSupportedException(SynacoreException):
    def __init__(self, opcode: Opcode):
        super().__init__(opcode)


class InvalidOpcodeException(SynacoreException):
    def __init__(self, opcode: Opcode):
        super().__init__(opcode)

class InvalidValueException(SynacoreException):
    def __init__(self, value: int):
        super().__init__(value)