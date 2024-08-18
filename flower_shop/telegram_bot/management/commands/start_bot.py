import os
import sys
import asyncio
import logging
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.types import BotCommand, BotCommandScopeDefault

class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **kwargs):
        # Установка переменной окружения для Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
        import django
        django.setup()

        # Инициализация бота
        API_TOKEN = '7369326068:AAGIKuTlGEoKO7i48YzgFNLyPKdc946pbSI'
        bot = Bot(token=API_TOKEN)

        # Инициализация хранилища состояний и диспетчера
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Инициализация роутера для обработки сообщений
        router = Router()
        dp.include_router(router)

        # Настройка логирования
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

        asyncio.run(main())
