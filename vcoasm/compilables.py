from abc import ABC, abstractmethod


class Compilable(ABC):
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def compile(self) -> bytearray:
        ...


class Raw(Compilable):
    def compile(self) -> bytearray:
        return bytearray([self.value])


class Integer(Compilable):
    def compile(self) -> bytearray:
        b = bytearray([0xF0])
        b.extend(self.value.to_bytes(8, "big"))
        return b


class String(Compilable):
    def compile(self) -> bytearray:
        b = bytearray([0xF1])
        b.extend(Integer(len(self.value)).compile())
        b.extend([ord(c) for c in self.value])
        return b


class DebugInfo(Compilable):
    def compile(self) -> bytearray:
        b = bytearray([0xFF])
        b.extend(String("@debug: " + self.value))
        return b
