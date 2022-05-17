from dataclasses import dataclass


@dataclass
class UserData:
    id: int
    name: str
    hashed_password: str
