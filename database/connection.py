from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import Base


# Подключение к sqlLite базе данных
DATABASE_URL = "sqlite+aiosqlite:///weather_data.db"

engine = create_async_engine(DATABASE_URL, future=True)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """инициализация бд"""
    async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


class SessionManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    async def __aenter__(self):
        # Создаем сессию при входе в контекст
        self.session = self.session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            # Если не было ошибок, зафиксируем изменения
            if exc_type is None:
                await self.session.commit()
            else:
                # Если возникли ошибки, откатим транзакцию
                await self.session.rollback()
        finally:
            # Закроем сессию в любом случае
            await self.session.close()
