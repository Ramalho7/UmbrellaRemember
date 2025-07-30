from models.model import Country, State, City, engine, Base, Session
import requests

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
        
if __name__ == "__main__":
    fetch_brazilian_cities_data()

