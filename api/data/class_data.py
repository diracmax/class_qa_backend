from dataclasses import dataclass


@dataclass
class ClassData:
    id: int
    name: str
    semester: str
    year: int