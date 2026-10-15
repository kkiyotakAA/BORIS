from dataclasses import dataclass


@dataclass
class Product:
    id: int | None
    name: str
    category: str
    sku: str
    quantity: int = 0


@dataclass
class Supplier:
    id: int | None
    name: str
    contact_person: str
    phone: str


@dataclass
class Operation:
    """Операция по складу: kind = 'in' (приёмка) или 'out' (отгрузка)."""
    id: int | None
    product_id: int
    supplier_id: int
    kind: str           # "in" | "out"
    amount: int