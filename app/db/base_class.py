from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr

class CustomBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Add common columns or methods here

class Base(DeclarativeBase, CustomBase):
    pass 