# db/conn.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_engine = None
_Session = None

def init_engine(database_url: str):
    global _engine, _Session
    _engine = create_engine(database_url, pool_pre_ping=True)
    _Session = sessionmaker(bind=_engine, autoflush=False, autocommit=False)

def get_session():
    if _Session is None:
        raise RuntimeError("DB engine is not initialized. Call init_engine() first.")
    return _Session()
