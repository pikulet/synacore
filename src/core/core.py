

class Synacore:

    def __init__(self, initial_memory: list[int]):
        self.__memory = Memory(initial_memory)
        self.__registers = Registers()
        self.__stack = Stack()
        self.__instruction_ptr = 0

    def run(self):
        while True:
            result = self.__run_next_instruction()
            match result:
                case Status.OK:
                    continue
                case Status.TERMINATED:
                    self.__output("success")
                    return
                case Status.ERROR:
                    self.__output("error_encountered")
                    return

    def __run_next_instruction(self) -> Status:
        opcode = self.__read_next_in_memory()

        match opcode:
            case Opcode.HALT:
                return self.__execute_halt()
            case Opcode.OUT:
                return self.__execute_out()


    def __read_next_in_memory(self) -> int:
        result = self.__memory.get(self.__instruction_ptr)
        self.__instruction_ptr += 1

    def __output(self, s):
        print(s)

    def __execute_halt(self) -> Status:
        return Status.TERMINATED

    def __execute_out(self) -> Status:
        a = self.__read_next_in_memory()
        result = chr(a)
        self.__output(result)
        return Status.OK

