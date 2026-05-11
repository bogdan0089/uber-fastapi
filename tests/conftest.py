import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from core.config import settings


TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    f"@{settings.DB_HOST}:{settings.DB_PORT}", "@localhost:5433"
).replace(settings.DB_NAME, settings.DB_NAME + "_test")


engine = create_async_engine(TEST_DATABASE_URL)
TestSessionMaker = async_sessionmaker(engine)


import database.database as db_module
db_module.async_session_maker = TestSessionMaker


from app.main import app
from database.database import get_session


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with TestSessionMaker() as s:
        yield s


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncClient:
    app.dependency_overrides[get_session] = lambda: session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users, trips, rating RESTART IDENTITY CASCADE"))
    yield
