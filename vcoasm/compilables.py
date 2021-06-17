from abc import ABC, abstractmethod


class Compilable(ABC):
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__} value={self.value}>"

    def __str__(self) -> str:
        return self.__repr__()

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
    def __init__(self, file: str, line: int) -> None:
        self.value = f"{line}@{file}"

    def compile(self) -> bytearray:
        b = bytearray([0xFF])
        b.extend(String(self.value).compile())
        return b
