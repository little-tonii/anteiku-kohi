from datetime import datetime


class MealEntity:
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    is_available: bool
    price: int
    image_url: str

    def __init__(self,
        id: int,
        name: str,
        description: str,
        created_at: datetime,
        updated_at: datetime,
        is_available: bool,
        price: int,
        image_url: str
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_available = is_available
        self.price = price
        self.image_url = image_url
