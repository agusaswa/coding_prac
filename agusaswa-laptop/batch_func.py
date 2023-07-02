from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int

class Batch:
    def __init__(
            self, ref: str, sku: str, 
            ava_qty: int, eta: Optional[date] = None
            )-> None:
        self.ref = ref
        self.sku = sku
        self.eta = eta
        self.ava_qty = ava_qty

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.ava_qty>=line.qty

    def allocate(self, line: OrderLine) -> None:
        self.ava_qty -= line.qty

    