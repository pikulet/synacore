from core.common.const import MODULO_BASE


class ALU:
    def sanitise(value: int) -> int:
        return value % MODULO_BASE

    @staticmethod
    def equals(a: int, b: int) -> int:
        return ALU.sanitise(int(a == b))

    @staticmethod
    def greater_than(a: int, b: int) -> int:
        return ALU.sanitise(int(a > b))

    @staticmethod
    def add(a: int, b: int) -> int:
        return ALU.sanitise(a + b)

    @staticmethod
    def mult(a: int, b: int) -> int:
        return ALU.sanitise(a * b)

    @staticmethod
    def mod(a: int, b: int) -> int:
        return ALU.sanitise(a % b)

    @staticmethod
    def bitwise_and(a: int, b: int) -> int:
        return ALU.sanitise(a & b)

    @staticmethod
    def bitwise_or(a: int, b: int) -> int:
        return ALU.sanitise(a | b)

    @staticmethod
    def bitwise_inverse(a: int) -> int:
        return ALU.sanitise(~a)
