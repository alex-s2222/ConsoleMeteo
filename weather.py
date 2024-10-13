import aiohttp
from datetime import datetime
import asyncio

from database.models import Weather
from database.connection import SessionManager, Session, init_db


# API ключ от OpenWeatherMap
API_KEY: str = "38fec43af62b54a4cd787bc6ed68d941"

# Координаты района Сколтеха
LAT: float = 55.7539
LON: float  = 37.6219

# URL для запроса данных погоды
URL: str = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=ru"


async def get_weather_data() -> dict:
    """Получаем данных из API"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(URL, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        return parse_weather_data(data)
                    else:
                        print(f"Error: Unable to fetch data (status code: {response.status})")
                        return None
        except TimeoutError as e:
            print("Сервер не отвечает")

                
        

def parse_weather_data(data) -> dict:
    """Фильтруем данных"""
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
    """Получаем направление ветра"""
    directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
    index = round(degrees / 45) % 8
    return directions[index]


async def save_db(data: dict) -> None:
    """Сохраняем в базу данных"""
    weather_record = Weather(**data)
    async with SessionManager(Session) as session:
        session.add(weather_record)


async def job() -> None:
    """Запускаем задачу"""
    weather_data = await get_weather_data()
    if weather_data:
        await save_db(weather_data)
        # print(f"Data saved at {weather_data['timestamp']}")


async def periodic_task(interval) -> None:
    """Запуск задач"""

    # создаем базу данных
    await init_db()

    #запускаем задачи
    while True:
        await job()
        await asyncio.sleep(interval)