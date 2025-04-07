from typing import Generator

from sqlmodel import Session

from core.database import get_session


async def get_db_session() -> Generator:
    session: Session = next(get_session())

    try:
        yield session
    finally:
        session.close()