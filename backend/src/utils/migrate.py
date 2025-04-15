import asyncio
from aerich import Command
from tortoise import Tortoise

from backend.src.config.aerich import TORTOISE_ORM


async def init_db():
    command: Command = Command(tortoise_config=TORTOISE_ORM)
    # 类似aerich init -t
    await command.init()
    try:
        # aerich init-db
        await command.init_db(safe=True)
        await command.migrate()
        await command.upgrade(run_in_transaction=True)
    except (FileExistsError, AttributeError):
        pass


async def lifespan():
    await init_db()
    await Tortoise.close_connections()


if __name__ == '__main__':
    asyncio.run(lifespan())
