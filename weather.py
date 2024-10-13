import aiohttp
from datetime import datetime
import asyncio

from pprint import pprint

from database.models import Weather

from database.connection import SessionManager, Session


# API ключ от OpenWeatherMap
API_KEY = "38fec43af62b54a4cd787bc6ed68d941"

# Координаты района Сколтеха
LAT = 55.7539
LON = 37.6219

# URL для запроса данных погоды
URL = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=ru"


async def get_weather_data() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            if response.status == 200:
                data = await response.json()
                return parse_weather_data(data)
            else:
                print(f"Error: Unable to fetch data (status code: {response.status})")
                return None
            

def parse_weather_data(data) -> dict:
    # Парсим необходимые данные
    temperature = data['main']['temp']
    wind_speed = data['wind']['speed']
    wind_direction = get_wind_direction(data['wind']['deg'])
    pressure = round(data['main']['pressure'] * 0.75006375541921, 2) # перевод из гПа в мм рт. ст.

    # Тип осадков и их количество
    precipitation_type = None
    precipitation_amount = 0

    if 'rain' in data:
        precipitation_type = "rain"
        precipitation_amount = data['rain'].get('1h', 0)
    elif 'snow' in data:
        precipitation_type = "snow"
        precipitation_amount = data['snow'].get('1h', 0)

    return {
        'timestamp': datetime.now(),
        'temperature': temperature,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'pressure': pressure,
        'precipitation_type': precipitation_type,
        'precipitation_amount': precipitation_amount
    }


def get_wind_direction(degrees) -> str:
    directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
    index = round(degrees / 45) % 8
    return directions[index]


async def save_db(data: dict):
    weather_record = Weather(**data)
    
    with SessionManager(Session) as session:
        session.add(weather_record)
        
        


async def job():
    weather_data = await get_weather_data()
    if weather_data:
        await save_db(weather_data)
        print(f"Data saved at {weather_data['timestamp']}")


async def periodic_task(interval):
    while True:
        await job()
        await asyncio.sleep(interval)