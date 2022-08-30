DELIMITER = ','

class Parser:

    @staticmethod
    def process(self, file: str) -> list[int]:
        with open(file, 'rb') as f:
            data = [int(x) for x in f.read().split(DELIMITER)]

        return data
