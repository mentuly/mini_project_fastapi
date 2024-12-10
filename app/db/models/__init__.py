from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from .. import engine


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


from .user import User
from .ads import AdsDB
from .. import Session


def up():
    Base.metadata.create_all(engine)


def down():
    Base.metadata.drop_all(engine)


down()
up()
