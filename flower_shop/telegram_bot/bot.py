from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import logging
import asyncio

API_TOKEN = '7369326068:AAGIKuTlGEoKO7i48YzgFNLyPKdc946pbSI'

# Установим уровень логирования
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработка команды /start
@dp.message(Command('start'))
async def send_welcome(message: Message):
    logging.info(f"Получена команда /start от {message.from_user.id}")
    await message.answer("Добро пожаловать! Как я могу помочь?")

# Обработка команды /help
@dp.message(Command('help'))
async def send_help(message: Message):
    logging.info(f"Получена команда /help от {message.from_user.id}")
    await message.answer("Помощь доступна по команде /start.")

# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  # Передаем объект бота в диспетчер

if __name__ == '__main__':
    asyncio.run(main())




# from aiogram import Bot, Dispatcher, F
# from aiogram.filters import Command
# from aiogram.types import Message
# import logging
# import asyncio
#
# API_TOKEN = '7369326068:AAGIKuTlGEoKO7i48YzgFNLyPKdc946pbSI'
#
# # Установим уровень логирования
# logging.basicConfig(level=logging.INFO)
#
# # Создаем объекты бота и диспетчера
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()
#
# # Обработка команды /start
# @dp.message(Command('start'))
# async def send_welcome(message: Message):
#     logging.info(f"Получена команда /start от {message.from_user.id}")
#     await message.answer("Привет! Я ваш бот!")
#
# # Обработка команды /help
# @dp.message(Command('help'))
# async def send_help(message: Message):
#     logging.info(f"Получена команда /help от {message.from_user.id}")
#     await message.answer("Помощь доступна по команде /start.")
#
# # Запуск бота
# async def main():
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)
#
# if __name__ == '__main__':
#     asyncio.run(main())