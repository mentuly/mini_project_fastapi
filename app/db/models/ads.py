from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from . import Base


class AdsDB(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(35))
    description: Mapped[str] = mapped_column(String(150))
    category: Mapped[str] = mapped_column(String(25))
    price: Mapped[float]
