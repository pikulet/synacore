class Parser:
    @staticmethod
    def process(file: str) -> list[int]:
        with open(file, "rb") as f:
            data = bytearray(f.read())

        return data
