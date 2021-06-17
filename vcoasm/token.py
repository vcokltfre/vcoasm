from dataclasses import dataclass

from .kw import keywords


@dataclass
class Token:
    type: str
    value: str

    file: str
    line: int

    @property
    def op(self):
        return keywords[self.value.upper()]
