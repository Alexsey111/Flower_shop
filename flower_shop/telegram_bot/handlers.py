from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.reply("Добро пожаловать! Как я могу помочь?")

@router.message(lambda message: "заказ" in message.text.lower())
async def handle_order(message: types.Message):
    await message.reply("Вы выбрали заказ. Пожалуйста, укажите детали.")
