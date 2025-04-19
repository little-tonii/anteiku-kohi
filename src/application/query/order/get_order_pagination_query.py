from ....domain.entity.meal_entity import MealEntity
from ....application.schema.response.order_response_schema import GetOrderByIdResponse, GetOrderPaginationResponse, OrderMealResponse
from ....domain.repository.order_repository import OrderRepository
from ....domain.repository.meal_repository import MealRepository

class GetOrderPaginationQuery:
    page: int
    size: int
    is_order_responsible: bool | None

    def __init__(self, page: int, size: int, is_order_responsible: bool | None):
        self.page = page
        self.size = size
        self.is_order_responsible = is_order_responsible

class GetOrderPaginationQueryHandler:
    order_repository: OrderRepository
    meal_repository: MealRepository

    def __init__(self, order_repository: OrderRepository, meal_repository: MealRepository):
        self.order_repository = order_repository
        self.meal_repository = meal_repository

    async def handle(self, query: GetOrderPaginationQuery) -> GetOrderPaginationResponse:
        orders = await self.order_repository.find_orders(page=query.page, size=query.size, is_order_responsible=query.is_order_responsible)
        orders_response: list[GetOrderByIdResponse] = []
        meal_lookup: dict[int, MealEntity] = {}
        for order in orders:
            order_meals = await self.order_repository.get_order_meal_list(order_id=order.id)
            for meal in order_meals:
                if meal.id in meal_lookup:
                    continue
                meal_result = await self.meal_repository.get_by_id(id=meal.meal_id)
                if meal_result:
                    meal_lookup[meal.meal_id] = meal_result
            orders_response.append(
                GetOrderByIdResponse(
                    id=order.id,
                    updated_at=order.updated_at,
                    created_at=order.created_at,
                    order_status=order.order_status,
                    payment_status=order.payment_status,
                    meals=[
                        OrderMealResponse(
                            id=order_meal.id,
                            price=order_meal.price,
                            quantity=order_meal.quantity,
                            name=meal_lookup[order_meal.meal_id].name,
                            description=meal_lookup[order_meal.meal_id].description,
                            image_url=meal_lookup[order_meal.meal_id].image_url,
                        )
                        for order_meal in order_meals
                    ],
                    staff_id=order.staff_id,
                )
            )
        return GetOrderPaginationResponse(
            orders=orders_response,
            page=query.page,
            size=query.size,
        )
