from core.common.const import *
from core.common.exception import SynacoreException
from core.common.util import Converter
from core.opcodes import Opcode
from core.memory import Memory
from core.registers import Registers
from core.stack import Stack
from core.alu import ALU
from core.io import IO


class Synacore:
    def __init__(self, initial_memory: bytearray):
        self.__memory = Memory(initial_memory)
        self.__registers = Registers(NUM_REGISTERS)
        self.__io = IO()
        self.__stack = Stack()
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
                case Opcode.SET:
                    return self.__execute_set()
                case Opcode.PUSH:
                    return self.__execute_push()
                case Opcode.POP:
                    return self.__execute_pop()
                case Opcode.EQ:
                    return self.__execute_eq()
                case Opcode.GT:
                    return self.__execute_gt()
                case Opcode.JMP:
                    return self.__execute_jmp()
                case Opcode.JT:
                    return self.__execute_jt()
                case Opcode.JF:
                    return self.__execute_jf()
                case Opcode.ADD:
                    return self.__execute_add()
                case Opcode.MULT:
                    pass
                case Opcode.MOD:
                    pass
                case Opcode.AND:
                    return self.__execute_and()
                case Opcode.OR:
                    return self.__execute_or()
                case Opcode.NOT:
                    return self.__execute_not()
                case Opcode.RMEM:
                    pass
                case Opcode.WMEM:
                    pass
                case Opcode.CALL:
                    pass
                case Opcode.RET:
                    pass
                case Opcode.OUT:
                    return self.__execute_out()
                case Opcode.IN:
                    pass
                case Opcode.NOOP:
                    return self.__execute_noop()

            raise OpcodeNotSupportedException(Opcode(opcode))

        except ValueError:
            raise InvalidOpcodeException(opcode)

    def __next(self):
        self.__instruction_ptr += 1

    ## getters
    def __read_next_raw_in_memory(self) -> bytearray:
        result = self.__memory.get(self.__instruction_ptr)
        self.__next()
        return result

    def __read_next_in_memory(self) -> int:
        return Converter.BytesToInt(self.__read_next_raw_in_memory())

    def __evaluate_next_in_memory(self) -> int:
        value = self.__read_next_in_memory()
        if value < MODULO_BASE:
            return value
        elif value <= REGISTER_MAX:
            return self.__registers.get(Converter.ValueToRegisterIndex(value))
        else:
            raise InvalidValueException(value)

    ## setters
    def __set_raw(self, address: int, value: bytearray):
        if address < MODULO_BASE:
            self.__memory.set(address, value)
        elif address <= REGISTER_MAX:
            self.__registers.set(Converter.ValueToRegisterIndex(address), value)
        else:
            raise InvalidValueException(value)

    def __set(self, address: int, value: int):
        return self.__set_raw(address, Converter.IntToBytes(value))

    def __output(self, s):
        self.__io.output(s)

    def __execute_halt(self) -> bool:
        """
        halt: 0
        stop execution and terminate the program
        """
        return True

    def __execute_set(self):
        """
        set: 1 a b
        set register <a> to the value of <b>
        """

        a = self.__read_next_in_memory()
        b = self.__read_next_raw_in_memory()

        index = Converter.ValueToRegisterIndex(a)
        self.__registers.set(index, b)

    def __execute_push(self):
        """
        push: 2 a
        push <a> onto the
        """
        a = self.__evaluate_next_in_memory()
        self.__stack.push(a)

    def __execute_pop(self):
        """
        pop: 3 a
        remove the top element from the stack and write it into <a>; empty stack = error
        """
        a = self.__read_next_in_memory()

        value = self.__stack.pop()
        self.__set(a, value)

    def __execute_eq(self):
        """
        eq: 4 a b c
        set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
        """
        a = self.__read_next_in_memory()
        b = self.__evaluate_next_in_memory()
        c = self.__evaluate_next_in_memory()

        result = ALU.equals(b, c)
        self.__set(a, result)

    def __execute_gt(self):
        """
        gt: 5 a b c
        set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
        """
        a = self.__read_next_in_memory()
        b = self.__evaluate_next_in_memory()
        c = self.__evaluate_next_in_memory()

        result = ALU.greater_than(b, c)
        self.__set(a, result)

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

    def __execute_add(self):
        """
        add: 9 a b c
        assign into <a> the sum of <b> and <c> (modulo 32768)
        """
        a = self.__read_next_in_memory()
        b = self.__evaluate_next_in_memory()
        c = self.__evaluate_next_in_memory()

        result = ALU.add(b, c)
        self.__set(a, result)

    def __execute_mult(self):
        """
        mult: 10 a b c
        store into <a> the product of <b> and <c> (modulo 32768)
        """
        pass

    def __execute_mod(self):
        """
        mod: 11 a b c
        store into <a> the remainder of <b> divided by <c>
        """
        pass

    def __execute_and(self):
        """
        and: 12 a b c
        stores into <a> the bitwise and of <b> and <c>
        """
        a = self.__read_next_in_memory()
        b = self.__evaluate_next_in_memory()
        c = self.__evaluate_next_in_memory()

        result = ALU.bitwise_and(b, c)
        self.__set(a, result)

    def __execute_or(self):
        """
        or: 13 a b c
        stores into <a> the bitwise or of <b> and <c>
        """
        a = self.__read_next_in_memory()
        b = self.__evaluate_next_in_memory()
        c = self.__evaluate_next_in_memory()

        result = ALU.bitwise_or(b, c)
        self.__set(a, result)

    def __execute_not(self):
        """
        not: 14 a b
        stores 15-bit bitwise inverse of <b> in <a>
        """
        a = self.__read_next_in_memory()
        b = self.__evaluate_next_in_memory()

        result = ALU.bitwise_inverse(b)
        self.__set(a, result)

    def __execute_rmem(self):
        """
        rmem: 15 a b
        read memory at address <b> and write it to <a>
        """
        pass

    def __execute_wmem(self):
        """
        wmem: 16 a b
        write the value from <b> into memory at address <a>
        """
        pass

    def __execute_call(self):
        """
        call: 17 a
        write the address of the next instruction to the stack and jump to <a>
        """
        pass

    def __execute_ret(self):
        """
        ret: 18
        remove the top element from the stack and jump to it; empty stack = halt
        """
        pass

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
