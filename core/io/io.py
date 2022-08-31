import sys


class IO:
    @staticmethod
    def output(s: str):
        sys.stdout.write(s)

    @staticmethod
    def input() -> str:
        return sys.stdin.readline()
