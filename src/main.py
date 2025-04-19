from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from fastapi import Request

from .presentation.websocket import order_websocket
from .presentation.api import order_api
from .infrastructure.config.variables import UPLOAD_FOLDER
from .presentation.api import meal_api
from .presentation.api import manager_api
from .presentation.api import user_api
from .infrastructure.config.database import init_db
from .infrastructure.config.exception_handler import process_http_exception, process_validation_error, process_global_exception

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

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

app.mount("/public/images", StaticFiles(directory=UPLOAD_FOLDER), name="images")

app.include_router(user_api.router)
app.include_router(manager_api.router)
app.include_router(meal_api.router)
app.include_router(order_api.router)

app.include_router(order_websocket.router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return process_http_exception(exc)

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return process_validation_error(exc)

@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, exc: RequestValidationError):
    return process_validation_error(exc)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return process_global_exception(exc)
