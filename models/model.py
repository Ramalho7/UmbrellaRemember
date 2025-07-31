from sqlalchemy import create_engine, Column, Integer, String, text, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv
import os
import requests
from argon2 import PasswordHasher
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin

ph = PasswordHasher()

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

Base = declarative_base()

Session = sessionmaker(bind=engine)

BRAZIL_TZ = timezone(timedelta(hours=-3))

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    country_name = Column(String(150), nullable=False)
    states = relationship("State", back_populates="country")
class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    state_name = Column(String(150), nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country", back_populates="states")
    cities = relationship("City", back_populates="state")
class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(150), nullable=False) 
    state_id = Column(Integer, ForeignKey('state.id'))
    state = relationship("State", back_populates="cities")
    users = relationship("User", back_populates="city")
class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City", back_populates="users")
    created_at = Column(
        String(30),
        nullable=False,
        default=lambda: datetime.now(BRAZIL_TZ).strftime('%Y-%m-%d %H:%M:%S')
    )

def create_tables():
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)

if __name__ == "__main__":
    create_tables()
    drop_tables()