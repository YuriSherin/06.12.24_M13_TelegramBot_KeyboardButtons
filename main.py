from info import token

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


api = token    # получить токен бота
bot = Bot(api)      # объект класса Bot()
dp = Dispatcher(bot, storage=MemoryStorage())   # диспетчер управления ботом

@dp.message_handler(commands=['start'])     # декоратор для обработки команды /start
async def start(message):
    """Асинхронный метод выполнения команды 'start'"""
    await message.answer(f'Здравствуйте! Рады Вас видеть в нашем боте!')

@dp.message_handler()                       # декоратор для обработки любых текстовых сообщений
async def all_messages(message):
    """Асинхронный метод отправки эхо-сообщений"""
    await message.answer(message.text.upper())








if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)       # запуск бота
