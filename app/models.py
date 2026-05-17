from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, text
from .database import Base

class Garage(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key= True, index = True)
    name = Column(String, nullable=False)
    power = Column(String, nullable=False)
    launched = Column(Date, nullable = False)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique = True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, server_default=text('now()'))

