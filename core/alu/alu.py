from core.common.const import MODULO_BASE


class ALU:
    def sanitise(value: int) -> int:
        return value % MODULO_BASE

    @staticmethod
    def add(a: int, b: int) -> int:
        return ALU.sanitise(a + b)

    @staticmethod
    def equals(a: int, b: int) -> int:
        return ALU.sanitise(int(a == b))

    @staticmethod
    def greater_than(a: int, b: int) -> int:
        return ALU.sanitise(int(a > b))