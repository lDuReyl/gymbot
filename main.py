import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.general import router as general_commands_router
from handlers.registration import router as registration_commands_router
from handlers.nutrients import router as nutrients_router
from callbacks.registration import router as callback_registration_router
from config_reader import config

dp = Dispatcher()
storage = MemoryStorage()

async def startup():
    print("Бот запущен")


async def main() -> None:
    bot = Bot(config.BOT_TOKEN.get_secret_value())
    dp.startup.register(startup)
    dp.include_routers(
        registration_commands_router,
        callback_registration_router,
        nutrients_router,
        general_commands_router
    )
    await dp.start_polling(bot, storage=storage, parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    asyncio.run(main())

