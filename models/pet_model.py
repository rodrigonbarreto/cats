from typing import Optional
from sqlmodel import Field, SQLModel


class PetModel(SQLModel, table=True):
    __tablename__: str = "pets"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    code_pet: str
    width: int
    height: int
    url: str
    name: str
