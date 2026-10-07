"""Initialize only the explicitly selected local SQLite test database."""
from uuid import UUID
from sqlalchemy import select
from app.core.database import engine, Base, AsyncSessionLocal
from app.core.config import settings
from app.models.db_models import User


PLACEHOLDER_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


async def initialize_local_test():
    if settings.local_test_mode:
        if engine.dialect.name != "sqlite":
            raise RuntimeError("LOCAL_TEST_MODE wymaga osobnej lokalnej bazy SQLite.")
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    # Do czasu logowania (etap 2) wszystkie analizy należą do jednego użytkownika zastępczego.
    # Na PostgreSQL tabele tworzy wcześniej `alembic upgrade head`.
    async with AsyncSessionLocal() as db:
        user_id = PLACEHOLDER_USER_ID
        if not (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none():
            db.add(User(id=user_id, sub="obsil-local-test", email="local-test@localhost", is_active=True))
            await db.commit()
