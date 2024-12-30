import asyncio
from typing import Final

from riko import Riko, configure_logging

from config import settings

logger = configure_logging()
TOKEN: Final[str] = settings["TOKEN"]


async def main() -> None:
    bot = Riko()
    await bot.start(TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt signal detected!")
