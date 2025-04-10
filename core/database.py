from sqlmodel import SQLModel, Session, create_engine

from core.configs import settings


engine = create_engine(settings.DB_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db():
    SQLModel.metadata.create_all(engine)