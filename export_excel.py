from sqlalchemy import select
import pandas as pd

from database.connection import SessionManager, Session
from database.models import Weather


def get_data_from_db(limit: int = 10) -> pd.DataFrame:
    """Получаем данные из базы данных"""
    query = select(Weather).order_by(Weather.timestamp.desc()).limit(limit)

    with SessionManager(Session) as session:
        data = session.scalars(query).all()
    
        df = pd.DataFrame([{
                'id': record.id,
                'Temperature': record.temperature,
                'Wind speed': record.wind_speed,
                'Wind direction': record.wind_direction,
                'Pressure': record.pressure,
                'Precipitation type': record.precipitation_type,
                'Precipitation amount': record.precipitation_amount,
                'Timestamp':record.timestamp
                } for record in data])
     
    return df


def export_to_excel(file_name: str) -> None:
    """Запись данных в Excel"""
    df = get_data_from_db()
    
    # Экспортируем в Excel
    df.to_excel(file_name + '.xlsx', index=False)
