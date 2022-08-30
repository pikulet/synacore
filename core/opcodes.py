from enum import Enum


class Opcode(Enum):
    HALT = 0
    SET = 1
    PUSH = 2
    POP = 3
    EQ = 4
    GT = 5
    JMP = 6
    JT = 7
    JF = 8
    ADD = 9
    MULT = 10
    MOD = 11
    AND = 12
    OR = 13
    NOT = 14
    OUT = 19
    NOOP = 21
