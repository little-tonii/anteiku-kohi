from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from .presentation.api import meal_api

from .presentation.api import manager_api

from .infrastructure.config.database import init_db

from .infrastructure.config.exception_handler import global_exception_handler, http_exception_handler, validation_exception_handler
from .presentation.api import user_api

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Anteiku Kohi", lifespan=lifespan)

origins = [
    "*"
]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_api.router)
app.include_router(manager_api.router)
app.include_router(meal_api.router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)