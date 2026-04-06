import asyncio

from app.core.database import Base, engine
from app.models import audit_log, invoice, invoice_item, user  # noqa: F401


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())
