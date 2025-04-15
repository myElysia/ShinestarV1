import os
from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM: dict = {
    "connections": {
        f"{os.getenv('DB_TYPE')}": {
            "engine": f"{os.getenv('DB_ENGINE')}",
            "credentials": {
                "host": f"{os.getenv('DB_HOST')}",
                "port": f"{os.getenv('DB_PORT')}",
                "user": f"{os.getenv('DB_USER')}",
                "password": f"{os.getenv('DB_PASS')}",
                "database": f"{os.getenv('DB_NAME')}",
            }
        }
    },
    "apps": {
        "models": ['backend.models', 'aerich.models'],
        "default_connection": "default",
    }
}