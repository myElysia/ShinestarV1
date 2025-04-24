import asyncio
from aerich import Command
from dotenv import load_dotenv
from tortoise import Tortoise

from src.config.tortoise import Settings

load_dotenv()

settings = Settings()


async def init_db():
    command: Command = Command(tortoise_config=settings.tortoise_config)
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
