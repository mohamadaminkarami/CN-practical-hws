from enum import Enum


class RType(int, Enum):
    A = 1


class RClass(int, Enum):
    IN = 1


class RCode(int, Enum):
    NO_ERROR = 0


class Opcode(int, Enum):
    STANDART_QUERY = 0
