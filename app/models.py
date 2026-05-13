from sqlalchemy import Column, Integer, String, Date
from . database import Base

class Garage(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key= True, index = True)
    name = Column(String, nullable=False)
    power = Column(String, nullable=False)
    launched = Column(Date, nullable = False)
    


