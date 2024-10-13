from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy import String, Integer, Float, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    pressure = Column(Float)
    precipitation_type = Column(String)
    precipitation_amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.now())

    def __str__(self):
        return f"{self.id} {self.temperature} {self.wind_speed} {self.wind_direction} {self.pressure} {self.precipitation_type} {self.precipitation_amount}"