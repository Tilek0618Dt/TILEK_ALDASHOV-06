from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import DATABASE_URL

# Render PostgreSQL URL адатта postgres://... келет
# SQLAlchemy async үчүн: postgresql+asyncpg://...
def _to_async_url(url: str) -> str:
    if url.startswith("postgresql+asyncpg://"):
        return url
    if url.startswith("postgres://"):
        return "postgresql+asyncpg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url[len("postgresql://"):]
    return url

ENGINE = create_async_engine(_to_async_url(DATABASE_URL), pool_pre_ping=True)
SessionLocal = async_sessionmaker(ENGINE, expire_on_commit=False, class_=AsyncSession)
