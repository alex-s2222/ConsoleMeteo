from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


# Подключение к MySQL базе данных
DATABASE_URL = "sqlite:///weather_data.db"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class SessionManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        # Создаем сессию при входе в контекст
        self.session = self.session_factory()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            # Если не было ошибок, зафиксируем изменения
            if exc_type is None:
                self.session.commit()
            else:
                # Если возникли ошибки, откатим транзакцию
                self.session.rollback()
        finally:
            # Закроем сессию в любом случае
            self.session.close()
