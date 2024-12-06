from info import token

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# импорты для работы машины состояний
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api = token    # получить токен бота
bot = Bot(api)      # объект класса Bot()
dp = Dispatcher(bot, storage=MemoryStorage())   # диспетчер управления ботом

class UserState(StatesGroup):
    """Дочерний класс, унаследованный от StatesGroup"""
    age  = State()      # возраст
    growth = State()    # рост
    weight = State()    # вес

@dp.message_handler(text='Calories')
async def set_age(message):
    """Эта функция выводит в Telegram-бот сообщение 'Введите свой возраст:'.
    и после этого ожидает ввода возраста в атрибут UserState.age при помощи метода set."""
    await message.answer('Введите свой возраст, лет:')
    await UserState.age.set()    # вызываем функцию установки возраста

@dp.message_handler(state=UserState.age)    # декоратор, указывает, что функция будет реагировать на state=UserState.age
async def set_growth(message, state):       # в функцию передаются уже два параметра
    """Эта функция обновляет данные в состоянии age на message.text, используя метод update_data.
    Далее выводит в Telegram-бот сообщение 'Введите свой рост:'.
    После этого ожидает ввода роста в атрибут UserState.growth при помощи метода set."""
    await state.update_data(age=message.text)       # обновим данные в состоянии age
    await message.answer('Введите свой рост, см.:') # выведем сообщение для пользователя
    await UserState.growth.set()                    # вызовем функцию установки веса


@dp.message_handler(state=UserState.growth) # декоратор, указывает, что функция будет реагировать на state=UserState.growth
async def set_weight(message, state):
    """Эта функция обновляет данные в состоянии growth на message.text (написанное пользователем сообщение),
    используя для этого метод update_data. Далее выводит в Telegram-бот сообщение 'Введите свой вес:'.
    После этого ожидает ввод веса в атрибут UserState.weight при помощи метода set."""
    await state.update_data(growth=message.text)    # обновим данные в состоянии growth
    await message.answer('Введите свой вес, кг.:')  # выведем сообщение для пользователя
    await UserState.weight.set()                    # вызовем функцию установки веса

@dp.message_handler(state=UserState.weight) # декоратор, указывает, что функция будет реагировать на state=UserState.weight
async def send_calories(message, state):
    """Эта функция обновляет данные в состоянии weight на message.text (написанное пользователем сообщение),
     используя для метод update_data. Далее в функции получает в переменную data все ранее введённые состояния
     при помощи метода state.get_data() и рассчитывает суточную норму калорий для мужчит и для женщин,
     отправляет результаты расчета в Телеграм и финиширует машину состояний методом finish()."""
    await  state.update_data(weight=message.text)   # обновим данные в состоянии weight
    data = await state.get_data()                   # получим наши данные из машины состояний

    # рассчитаем суточную номру калорий для мужчин и для женщин
    calories_men = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    calories_women = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161

    # сформируем сообщение для пользователя и выведем его в Телеграмм
    msg = f'Суточная норма калорий:\n    Для мужчин: {str(calories_men)},\n    Для женщин: {str(calories_women)}'
    await message.answer(msg)

    await state.finish()    # завершим работу с машиной состояний

# для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
# для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)       # запуск бота
