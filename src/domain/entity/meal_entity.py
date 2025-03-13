from datetime import datetime


class MealEntity:
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    is_avaiable: bool
    price: int
    
    def __init__(self,
        id: int,
        name: str,
        description: str,
        created_at: datetime,
        updated_at: datetime,
        is_avaiable: bool,
        price: int
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_avaiable = is_avaiable
        self.price = price