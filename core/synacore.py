from core.common.const import *
from core.common.exception import SynacoreException
from core.common.util import Converter
from core.opcodes import Opcode
from core.memory import Memory
from core.registers import Registers
from core.stack import Stack
from core.alu import ALU
from core.io import IO

from logger import Logger


class Synacore:
    def __init__(self, initial_memory: bytearray):
        self.__memory = Memory(initial_memory)
        self.__registers = Registers(NUM_REGISTERS)
        self.__io = IO()
        self.__stack = Stack()
        self.__instruction_ptr = 0
        self.__logger = Logger()

    def run(self):
        self.__instruction_ptr = 0
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
            opcode = self.__read_next_address_in_memory()
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
                    return self.__execute_mult()
                case Opcode.MOD:
                    return self.__execute_mod()
                case Opcode.AND:
                    return self.__execute_and()
                case Opcode.OR:
                    return self.__execute_or()
                case Opcode.NOT:
                    return self.__execute_not()
                case Opcode.RMEM:
                    return self.__execute_rmem()
                case Opcode.WMEM:
                    return self.__execute_wmem()
                case Opcode.CALL:
                    return self.__execute_call()
                case Opcode.RET:
                    return self.__execute_ret()
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

    def __read_next_address_in_memory(self) -> int:
        result = Converter.BytesToInt(self.__read_next_raw_in_memory())
        return result

    def __evaluate_next_literal_in_memory(self) -> int:
        value = self.__read_next_address_in_memory()
        self.__logger.debug("           | address", self.__instruction_ptr - 1, "literal", value)
        if value < MODULO_BASE:
            return value
        elif value <= REGISTER_MAX:
            data = self.__registers.get(Converter.ValueToRegisterIndex(value))
            return Converter.BytesToInt(data)
        else:
            raise InvalidValueException(value)

    def __get_raw(self, address: int) -> bytearray:
        if address < MODULO_BASE:
            return self.__memory.get(address)
        elif address <= REGISTER_MAX:
            return self.__registers.get(Converter.ValueToRegisterIndex(address))
        else:
            raise InvalidAddressException(address)

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
        # self.__io.output(s)
        pass

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

        self.__logger.debug("set")
        a = self.__read_next_address_in_memory()
        b = self.__read_next_raw_in_memory()
        self.__logger.debug("       args", a, b)

        index = Converter.ValueToRegisterIndex(a)
        self.__registers.set(index, b)

    def __execute_push(self):
        """
        push: 2 a
        push <a> onto the
        """
        self.__logger.debug("push")
        a = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a)

        self.__stack.push(a)

    def __execute_pop(self):
        """
        pop: 3 a
        remove the top element from the stack and write it into <a>; empty stack = error
        """
        self.__logger.debug("pop")
        a = self.__read_next_address_in_memory()
        self.__logger.debug("       args", a)

        value = self.__stack.pop()
        self.__logger.debug("       result", value)

        self.__set(a, value)

    def __execute_eq(self):
        """
        eq: 4 a b c
        set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
        """
        self.__logger.debug("eq")
        a = self.__read_next_address_in_memory()
        b = self.__evaluate_next_literal_in_memory()
        c = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a, b, c)

        result = ALU.equals(b, c)
        self.__logger.debug("       result", result)

        self.__set(a, result)

    def __execute_gt(self):
        """
        gt: 5 a b c
        set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
        """
        self.__logger.debug("gt")
        a = self.__read_next_address_in_memory()
        b = self.__evaluate_next_literal_in_memory()
        c = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a, b, c)

        result = ALU.greater_than(b, c)
        self.__logger.debug("       result", result)

        self.__set(a, result)

    def __execute_jmp(self):
        """
        jmp: 6 a
        jump to <a>
        """
        self.__logger.debug("jmp")
        a = self.__read_next_address_in_memory()
        self.__logger.debug("       args", a)

        self.__instruction_ptr = a

    def __execute_jt(self):
        """
        jt: 7 a b
        if <a> is nonzero, jump to <b>
        """
        self.__logger.debug("jt")
        a = self.__evaluate_next_literal_in_memory()
        b = self.__read_next_address_in_memory()
        self.__logger.debug("       args", a, b)

        if a != 0:
            self.__instruction_ptr = b

    def __execute_jf(self):
        """
        jf: 8 a b
        if <a> is zero, jump to <b>
        """
        self.__logger.debug("jf")
        a = self.__evaluate_next_literal_in_memory()
        b = self.__read_next_address_in_memory()
        self.__logger.debug("       args", a, b)

        if a == 0:
            self.__instruction_ptr = b

    def __execute_add(self):
        """
        add: 9 a b c
        assign into <a> the sum of <b> and <c> (modulo 32768)
        """
        self.__logger.debug("add")
        a = self.__read_next_address_in_memory()
        b = self.__evaluate_next_literal_in_memory()
        c = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a, b, c)

        result = ALU.add(b, c)
        self.__logger.debug("       result", result)
        self.__set(a, result)

    def __execute_mult(self):
        """
        mult: 10 a b c
        store into <a> the product of <b> and <c> (modulo 32768)
        """
        self.__logger.debug("mult")
        a = self.__read_next_address_in_memory()
        b = self.__evaluate_next_literal_in_memory()
        c = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a, b, c)

        result = ALU.mult(b, c)
        self.__logger.debug("       result", result)
        self.__set(a, result)

    def __execute_mod(self):
        """
        mod: 11 a b c
        store into <a> the remainder of <b> divided by <c>
        """
        self.__logger.debug("mod")
        a = self.__read_next_address_in_memory()
        b = self.__evaluate_next_literal_in_memory()
        c = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a, b, c)

        result = ALU.mod(b, c)
        self.__logger.debug("       result", result)
        self.__set(a, result)

    def __execute_and(self):
        """
        and: 12 a b c
        stores into <a> the bitwise and of <b> and <c>
        """
        self.__logger.debug("add")
        a = self.__read_next_address_in_memory()
        b = self.__evaluate_next_literal_in_memory()
        c = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a, b, c)

        result = ALU.bitwise_and(b, c)
        self.__logger.debug("       result", result)

        self.__set(a, result)

    def __execute_or(self):
        """
        or: 13 a b c
        stores into <a> the bitwise or of <b> and <c>
        """
        self.__logger.debug("or")
        a = self.__read_next_address_in_memory()
        b = self.__evaluate_next_literal_in_memory()
        c = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a, b, c)

        result = ALU.bitwise_or(b, c)
        self.__logger.debug("       result", result)

        self.__set(a, result)

    def __execute_not(self):
        """
        not: 14 a b
        stores 15-bit bitwise inverse of <b> in <a>
        """
        self.__logger.debug("not")
        a = self.__read_next_address_in_memory()
        b = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a, b)

        result = ALU.bitwise_inverse(b)
        self.__logger.debug("       result", result)

        self.__set(a, result)

    def __execute_rmem(self):
        """
        rmem: 15 a b
        read memory at address <b> and write it to <a>
        """
        self.__logger.debug("rmem")
        a = self.__read_next_address_in_memory()
        b = self.__read_next_address_in_memory()
        self.__logger.debug("       args", a, b)

        value = self.__get_raw(b)
        self.__logger.debug("       result", value)
        self.__set_raw(a, value)

    def __execute_wmem(self):
        """
        wmem: 16 a b
        write the value from <b> into memory at address <a>
        """
        a = self.__read_next_address_in_memory()
        b = self.__evaluate_next_literal_in_memory()
        self.__set(a, b)

    def __execute_call(self):
        """
        call: 17 a
        write the address of the next instruction to the stack and jump to <a>
        """
        self.__logger.debug("call")
        a = self.__evaluate_next_literal_in_memory()
        self.__logger.debug("       args", a)

        self.__stack.push(self.__instruction_ptr)
        self.__instruction_ptr = a

    def __execute_ret(self):
        """
        ret: 18
        remove the top element from the stack and jump to it; empty stack = halt
        """
        self.__logger.debug("ret")
        value = Converter.BytesToInt(self.__stack.pop())
        self.__instruction_ptr = value

    def __execute_out(self):
        """
        out: 19 a
        write the character represented by ascii code <a> to the terminal
        """
        a = self.__evaluate_next_literal_in_memory()
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


class InvalidAddressException(SynacoreException):
    def __init__(self, address: int):
        super().__init__(address)
