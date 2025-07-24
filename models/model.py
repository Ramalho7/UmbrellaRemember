from sqlalchemy import create_engine, Column, Integer, String, text, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

Base = declarative_base()
class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    country_name = Column(String(150), nullable=False)
class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    state_name = Column(String(150), nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("country", back_populates="State")
class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(150), nullable=False) 
    state_id = Column(Integer, ForeignKey('state.id'))
    state = relationship("State", back_populates="City")
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City", back_populates="users")

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()