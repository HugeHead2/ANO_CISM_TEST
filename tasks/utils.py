import os
from typing import Optional


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.environ.get(name, None)

    if value is None and default is not None:
        return default

    if value is None and default is None:
        raise ValueError(f"Setting {name} not found. Set in configuration")

    return value


def get_connection_string():
    return f"postgresql+asyncpg://{get_env('DB_USER')}:{get_env('DB_PASS')}@{get_env('DB_HOST')}/{get_env('DB_NAME')}"
