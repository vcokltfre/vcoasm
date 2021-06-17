from typing import List
from regex import compile as re_compile

from loguru import logger

from .token import Token
from .kw import keywords


NUM_RE = re_compile(r"^\d+$")
IDT_RE = re_compile(r"^[a-zA-Z]+$")


class Lexer:
    """A simple lexer for vcoasm."""

    def __init__(self, file: str, code: str) -> None:
        self.file = file
        self.code = code

        self.lines = [line.strip() for line in code.split("\n")]
        self.tokens: List[Token] = []

    def _tokenize_line(self, lineno: int, line: str) -> List[Token]:
        build = ""
        string = False
        raw_tokens = []

        for i, letter in enumerate(line):
            if letter == '"' and not string:
                string = True
                build += letter
            elif letter == '"' and string and build and build[-1] == "\\":
                build += letter
            elif letter == '"':
                string = False
                build += letter
            elif letter == ";" and not string:
                break
            elif letter == " ":
                raw_tokens.append(build)
                build = ""
            elif i == len(line) - 1:
                build += letter
                raw_tokens.append(build)
                build = ""
            else:
                build += letter

        tokens = []

        for token in raw_tokens:
            if token.startswith('"'):
                # String
                tokens.append(Token("string", token, self.file, lineno))
                continue
            elif IDT_RE.match(token):
                tokens.append(Token("identifier", token, self.file, lineno))
                continue
            token = token.upper()
            if token in keywords:
                tokens.append(Token("keyword", token, self.file, lineno))
            elif token == "GT":
                tokens.append(Token("goto", None, self.file, lineno))
            elif token == "VAR":
                tokens.append(Token("var", None, self.file, lineno))
            elif NUM_RE.match(token):
                tokens.append(Token("number", token, self.file, lineno))
            else:
                logger.warning("Oh no?")

        return tokens

    def tokenize(self) -> None:
        for i, line in enumerate(self.lines):
            self.tokens.extend(self._tokenize_line(i, line))
