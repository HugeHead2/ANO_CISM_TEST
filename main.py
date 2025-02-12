from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

from tasks.routes.tasks import router as tasks


def include_routes(app: FastAPI) -> FastAPI:
    app.include_router(tasks)
    return app


async def not_found_exception_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=404,
        content="Not found"
    )


def incldue_exception_handlers(app: FastAPI) -> FastAPI:
    app.add_exception_handler(500, not_found_exception_handler)
    return app


def build_app_main() -> FastAPI:
    app = FastAPI(
        root_path="/api/v1"
    )
    app = include_routes(app)
    app = incldue_exception_handlers(app)
    return app


app = build_app_main()