from typing import List

from .compilables import Compilable, Raw, Integer, String, DebugInfo, Identifier
from .token import Token


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens

    @staticmethod
    def validate_line(line: List[Token]) -> bool:
        return True

    def generate_compilables(self) -> List[Compilable]:
        compilables = []
        segment = []

        c_append = compilables.append

        cline = 0
        c_append(DebugInfo(self.tokens[0].file, cline))

        for token in self.tokens:
            if token.line > cline:
                cline = token.line
                c_append(DebugInfo(self.tokens[0].file, cline))
                if not self.validate_line(segment):
                    raise Exception()  # TODO: Better exceptions
                segment = []

            segment.append(token)

            if token.type == "keyword":
                c_append(Raw(token.op))
            elif token.type == "string":
                c_append(String(token.value))
            elif token.type == "number":
                c_append(Integer(int(token.value)))
            elif token.type == "var":
                c_append(Raw(0xF2))
            elif token.type == "goto":
                c_append(Raw(0xF3))
            elif token.type == "identifier":
                c_append(Identifier(token.value))

        return compilables
