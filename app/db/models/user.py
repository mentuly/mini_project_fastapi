from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from . import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    login: Mapped[int] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
