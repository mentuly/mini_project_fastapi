from ..db import Config


def get_session():
    with Config.ENGINE.begin() as session:
        yield session
