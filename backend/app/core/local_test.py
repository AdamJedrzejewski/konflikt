"""Initialize only the explicitly selected local SQLite test database."""
from uuid import UUID
from sqlalchemy import select
from app.core.database import engine, Base, AsyncSessionLocal
from app.core.config import settings
from app.models.db_models import User


async def initialize_local_test():
    if not settings.local_test_mode:
        return
    if engine.dialect.name != "sqlite":
        raise RuntimeError("LOCAL_TEST_MODE wymaga osobnej lokalnej bazy SQLite.")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        user_id = UUID("00000000-0000-0000-0000-000000000001")
        if not (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none():
            db.add(User(id=user_id, sub="obsil-local-test", email="local-test@localhost", is_active=True))
            await db.commit()
