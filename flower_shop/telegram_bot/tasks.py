import asyncio
import logging
from aiogram import Bot
from django.conf import settings
from asgiref.sync import async_to_sync
from django.db import models

API_TOKEN = settings.TELEGRAM_API_TOKEN

logging.basicConfig(level=logging.INFO)

# Создание объекта бота
bot = Bot(token=API_TOKEN)


async def send_telegram_message(chat_id, text):
    """
    Отправляет сообщение в Telegram.

    :param chat_id: Идентификатор чата в Telegram (например, ID пользователя).
    :param text: Текст сообщения.
    """
    try:
        await bot.send_message(chat_id, text)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")


async def send_order_status_notification(order_id):
    """
    Отправляет уведомление о статусе заказа.

    :param order_id: ID заказа.
    """
    # Импортируем модель и находим заказ по ID
    from flower_shop.shop.models import Order
    try:
        order = Order.objects.get(id=order_id)
        user_profile = order.user.profile

        # Проверяем, есть ли у пользователя номер телефона для отправки сообщения
        if user_profile.phone:
            message = f"Ваш заказ #{order.id} теперь имеет статус: {order.get_status_display()}."
            await send_telegram_message(user_profile.phone, message)
        else:
            logging.warning(f"У пользователя {order.user.username} отсутствует номер телефона для отправки сообщения.")
    except Order.DoesNotExist:
        logging.error(f"Заказ с ID {order_id} не найден.")
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")

# Пример вызова задачи, если вам нужно вызвать её из другого места в вашем коде
# async_to_sync(send_order_status_notification)(order_id)


# import asyncio
# import logging
# from aiogram import Bot, Dispatcher, Router, types
# from aiogram.filters import Command
# from django.conf import settings
#
# API_TOKEN = settings.TELEGRAM_API_TOKEN
#
# logging.basicConfig(level=logging.INFO)
#
# # Создание бота и диспетчера
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()
#
# # Создание маршрутизатора и добавление его в диспетчер
# router = Router()
# dp.include_router(router)
#
# # Пример обработки команды /start
# @router.message(Command('start'))
# async def start_message(message: types.Message):
#     await message.reply("Здравствуйте! Я ваш бот.")
#
# async def on_startup():
#     logging.info("Бот запущен")
#
# async def on_shutdown():
#     logging.info("Бот выключается")
#
# # Запуск бота
# async def main():
#     dp.startup.register(on_startup)
#     dp.shutdown.register(on_shutdown)
#     # Запускаем polling
#     await dp.start_polling(skip_updates=True)
#
# if __name__ == '__main__':
#     asyncio.run(main())
#
# # Вспомогательная функция для отправки сообщений
# async def send_telegram_message(chat_id, text):
#     bot = Bot(token=settings.TELEGRAM_API_TOKEN)
#     await bot.send_message(chat_id, text)
#     await bot.session.close()  # Закрываем сессию после отправки сообщения




