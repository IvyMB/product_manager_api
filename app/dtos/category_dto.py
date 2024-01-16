from dataclasses import dataclass


@dataclass
class CategoryDTO:
    title: str
    description: str
    owner_id: str
