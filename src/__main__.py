from asyncio.runners import run
from os import environ
from dotenv import load_dotenv

from aiogram.client.bot import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers import general
from src.handlers.call_handler import general_call

load_dotenv("./secrets/main.env", override=True)

if __name__ == '__main__':
    async def main() -> None:
        dp = Dispatcher(storage=MemoryStorage())
        bot = Bot(
            token=environ.get("BOT_TOKEN")
        )

        dp.include_routers(general.router,
                           general_call.router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    try:
        print("Bot Started")
        run(main())
    except KeyboardInterrupt:
        ...
