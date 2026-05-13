from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_URL = "postgresql://postgres:123456@localhost/FastAPI_Learning"          #postgresql://username:password@server_name/database_name

engine = create_engine(SQL_ALCHEMY_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
