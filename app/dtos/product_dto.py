from dataclasses import dataclass


@dataclass
class ProductDTO:
    title: str
    description: str
    price: float
    owner_id: str
    category: str
