from datetime import datetime


class OrderMealEntity:
    id: int
    order_id: int
    meal_id: int
    price: int
    quantity: int
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        id: int,
        order_id: int,
        meal_id: int,
        price: int,
        quantity: int,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.order_id = order_id
        self.meal_id = meal_id
        self.price = price
        self.quantity = quantity
        self.created_at = created_at
        self.updated_at = updated_at
