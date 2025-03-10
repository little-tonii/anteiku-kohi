from typing import Annotated

from fastapi import Depends
from application.command.staff.create_staff_command import CreateStaffCommand, CreateStaffCommandHandler
from application.query.staff.get_staff_by_email_query import GetStaffByEmailQuery, GetStaffByEmailQueryHandler
from application.query.staff.get_staff_by_id_query import GetStaffByIdQuery, GetStaffByIdQueryHandler
from application.schema.response.user_response_schema import CreateStaffResponse, GetStaffByEmailResponse, GetStaffByIdResponse


class StaffService:
    
    @classmethod
    async def get_staff_by_id_task(query_handler: Annotated[GetStaffByIdQueryHandler, Depends()], id: int) -> GetStaffByIdResponse:
        query = GetStaffByIdQuery(id=id)
        result = await query_handler.handle(query=query)
        return result
    
    @classmethod
    async def get_staff_by_email_task(query_handler: Annotated[GetStaffByEmailQueryHandler, Depends()], email: str) -> GetStaffByEmailResponse:
        query = GetStaffByEmailQuery(email=email)
        result = await query_handler.handle(query=query)
        return result
    
    @classmethod
    async def create_staff_task(command_handler: Annotated[CreateStaffCommandHandler, Depends()], full_name: str, phone_number: str, email: str, address: str, password: str) -> CreateStaffResponse:
        command = CreateStaffCommand(
            
        )