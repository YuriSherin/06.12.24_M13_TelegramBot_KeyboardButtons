from info import token

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


api = token    # получить токен бота
bot = Bot(api)      # объект класса Bot()
dp = Dispatcher(bot, storage=MemoryStorage())   # диспетчер управления ботом

@dp.message_handler(commands=['start'])     # декоратор для обработки команды /start
async def start(message):
    print(f'Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler()                       # декоратор для обработки любых текстовых сообщений
async def all_messages(message):
    print(f'Введите команду /start, чтобы начать общение.')







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)       # запуск бота
