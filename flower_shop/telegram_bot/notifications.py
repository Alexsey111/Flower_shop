from aiogram import Bot

async def send_order_status_update(bot: Bot, chat_id: int, order_id: int, status: str):
    message = f"Ваш заказ #{order_id} был обновлен. Новый статус: {status}."
    await bot.send_message(chat_id=chat_id, text=message)
