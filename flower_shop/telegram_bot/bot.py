from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.types import BotCommand, BotCommandScopeDefault
import logging
import asyncio
from flower_shop.telegram_bot.handlers import router

API_TOKEN = '7369326068:AAGIKuTlGEoKO7i48YzgFNLyPKdc946pbSI'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

logging.basicConfig(level=logging.INFO)

async def on_startup(dispatcher: Dispatcher):
    logging.info("Бот запущен")
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

async def on_shutdown(dispatcher: Dispatcher):
    logging.info("Бот остановлен")

async def main():
    await on_startup(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(dp)

if __name__ == '__main__':
    asyncio.run(main())
