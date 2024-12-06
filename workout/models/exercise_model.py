from dataclasses import dataclass

from datetime import date

@dataclass
class Exercise:
    name: str
    muscle_group: int
    equipment: str
    date: date