from os import stat


class Converter:
    @staticmethod
    def BytesToInt(b: bytearray) -> int:
        return int.from_bytes(b, "little", signed="false")

    @staticmethod
    def IntToBytes(d: int) -> bytearray:
        pass
