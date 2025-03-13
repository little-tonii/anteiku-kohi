from ...domain.repository.meal_repository import MealRepository


class MealService:
    meal_repository: MealRepository
    
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository