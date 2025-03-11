from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from contextlib import asynccontextmanager
bot_username = "wiki_koha_bot"
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/animebot"
engine = create_async_engine(DATABASE_URL, echo=True)

# Asinxron session
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Model bazasi
Base = declarative_base()


# Asinxron session generator
@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
