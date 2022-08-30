from .const import ENDIANNESS, MODULO_BASE, NUM_BYTES_PER_WORD, NUM_REGISTERS, SIGNED


class Converter:
    @staticmethod
    def BytesToInt(b: bytearray) -> int:
        result = int.from_bytes(b, byteorder=ENDIANNESS, signed=SIGNED)
        return result

    @staticmethod
    def IntToBytes(d: int) -> bytearray:
        return d.to_bytes(
            length=NUM_BYTES_PER_WORD, byteorder=ENDIANNESS, signed=SIGNED
        )

    @staticmethod
    def ValueToRegisterIndex(value: int) -> int:
        result = value - MODULO_BASE
        if result < 0 or result >= NUM_REGISTERS:
            raise InvalidRegisterIndexException(result)
        return result


class InvalidRegisterIndexException(Exception):
    def __init__(self, index: int):
        super().__init__(index)
