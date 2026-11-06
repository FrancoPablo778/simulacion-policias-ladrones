
from dataclasses import dataclass


@dataclass
class Prisoner:
    position: tuple[int, int]
    state: str = "free"


@dataclass
class Police:
    position: tuple[int, int]
    target: int = -1
    escorting: int = -1
