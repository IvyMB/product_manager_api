from dataclasses import dataclass
from typing import Optional


@dataclass
class UserDTO:
    username: str
    email: str
    password: str
    store_id: Optional[str] = None
    active: bool = True
