from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str

    file: str
    line: int
