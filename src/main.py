from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.config.exception_handler import global_exception_handler, http_exception_handler
from presentation.api import staff_api

app = FastAPI(title="Anteiku Kohi")

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

app.include_router(staff_api.router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)