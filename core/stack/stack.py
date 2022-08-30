from core.common.exception import SynacoreException

class Stack:

    def __init__(self):
        self.__data = list()

    def push(self, value: bytearray):
        self.__data.append(value)

    def pop(self) -> bytearray:
        if len(self.__data) == 0:
            raise StackUnderflowException()

        return self.__data.pop()

class StackUnderflowException(SynacoreException):
    pass
