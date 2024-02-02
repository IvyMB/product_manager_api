from dataclasses import dataclass
from typing import Optional, List


@dataclass
class UserDTO:
    username: str
    email: str
    password: str
    roles: List[str]
    store_id: Optional[str] = None
    active: bool = True
