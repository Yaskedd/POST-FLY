import asyncio
import logging
import sys
from os import getenv

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot_instance import bot
from handlers.routes import router
from middlewares.subscription_verification import is_subscribe

load_dotenv()
TOKEN = getenv('BOT_TOKEN')
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)
dispatcher.include_router(router)
dispatcher.message.middleware(is_subscribe())
async def main() -> None:
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
