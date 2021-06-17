from pathlib import Path
from typing import Union

from .lexer import Lexer
from .parser import Parser


def compile(path: Union[str, Path]) -> bytearray:
    with Path(path).open() as f:
        lexer = Lexer(str(path), f.read())
    lexer.tokenize()
    parser = Parser(lexer.tokens)
    compilables = parser.generate_compilables()
    byte_values = bytearray()
    for c in compilables:
        byte_values.extend(c.compile())
    return byte_values
