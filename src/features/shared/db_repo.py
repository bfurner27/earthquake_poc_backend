from enum import Enum
from typing import Optional

class Order(Enum):
    DESC = 1,
    ASC = 2,


class OrderBy:
    field: str
    order: Order

    def __init__(self, field: str, order: Order = Order.ASC):
        self.field = field
        self.order = order

class ReadParamsBase:
    offset: int = 0
    limit: int = 100
    orderBy: OrderBy | None = None

    def __init__(self, offset: int = 0, limit: int = 100, orderBy: Optional[OrderBy] = None):
        self.offset = offset
        self.limit = limit
        
        if (orderBy != None):
            self.orderBy = orderBy

        if (id != None):
            self.id = id