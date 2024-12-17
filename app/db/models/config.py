from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Config:
    ENGINE = create_engine("sqlite:///my_db.db", echo=True)
    SESSION = sessionmaker(ENGINE)
