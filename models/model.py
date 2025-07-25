from sqlalchemy import create_engine, Column, Integer, String, text, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv
import os
import requests
from argon2 import PasswordHasher
from datetime import datetime, timedelta, timezone


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
class User(Base):
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

    def set_password(self, password_plain):
        self.password = ph.hash(password_plain)

    def check_password(self, password_plain):
        try:
            return ph.verify(self.password, password_plain)
        except Exception:
            return False
def create_tables():
    Base.metadata.create_all(engine)



def fetch_brazilian_cities_data():
    session = Session()
    try:
        brazil = Country(id=1, country_name="Brazil")
        session.add(brazil)
        session.commit()
        
        states_url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        states_response = requests.get(states_url)
        states_response.raise_for_status()
        states = states_response.json()
        
        for state in states:
            state_entry = State(
                id=state['id'],
                state_name=state['nome'],
                country_id=1
            )
            session.add(state_entry)
            session.commit()
            
            city_url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state['id']}/municipios"
            city_response = requests.get(city_url)
            city_response.raise_for_status()
            cities = city_response.json()
            
            for city in cities:
                city_entry = City(
                    id=city['id'],
                    city_name=city['nome'],
                    state_id=state['id']
                )
                session.add(city_entry)
                session.commit()
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from IBGE API: {e}")
        session.rollback()
    except Exception as e:
        print(f"Error populating database: {e}")
        session.rollback()
    finally:
        session.close()

def drop_tables():
    Base.metadata.drop_all(engine)

if __name__ == "__main__":
    create_tables()
    fetch_brazilian_cities_data()
    #drop_tables()