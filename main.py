import info
from info import token

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


api = info.token    # получить токен бота
bot = Bot(api)      # объект класса Bot()
dp = Dispatcher(bot, storage=MemoryStorage())   # диспетчер управления ботом









if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)       # запуск бота
