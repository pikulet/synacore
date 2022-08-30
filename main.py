from core import Synacore
from parser import Parser

if __name__ == '__main__':
    data = Parser.process('challenge.bin')
    synacore = Synacore(data)
    synacore.run()