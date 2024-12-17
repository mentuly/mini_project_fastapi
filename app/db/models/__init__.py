from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


from .user import User
from .ads import AdsDB
from .config import Config

Sessions = Config.SESSION


def up():
    Base.metadata.create_all(Config.ENGINE)


def down():
    Base.metadata.drop_all(Config.ENGINE)


def migrate():
    down()
    up()
